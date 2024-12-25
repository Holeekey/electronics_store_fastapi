from asyncio import sleep
import asyncio
import time
from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4, BaseModel

from common.application.decorators.error_decorator import ErrorDecorator
from common.application.decorators.logger_decorator import LoggerDecorator
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from common.domain.utils.is_not_none import is_not_none
from common.infrastructure.auth.get_current_user import get_current_user
from common.infrastructure.auth.models.auth_user import AuthUser, AuthUserRole
from common.infrastructure.auth.role_checker import role_checker
from common.infrastructure.bus.bus import Bus, get_command_bus
from common.infrastructure.database.database import get_session
from common.infrastructure.database.mongo import get_mongo_client
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.loggers.loguru_logger import LoguruLogger
from common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from common.infrastructure.token.jwt.jwt_provider import get_jwt_provider
from common.infrastructure.cryptography.fernet_cryptography_provider import get_fernet_provider
from user.application.commands.create.create_user_command import CreateUserCommand
from user.application.commands.delete.delete_manager_command import DeleteManagerCommand
from user.application.commands.delete.types.dto import DeleteManagerDto
from user.application.commands.login.login_command import LoginCommand
from user.application.commands.update.update_user_command import UpdateUserCommand
from user.application.info.user_found_info import user_found_info
from user.application.models.user import UserRole
from user.application.queries.find_all.find_all_managers_query import FindAllManagersQuery
from user.application.queries.find_one.find_one_user_query import FindOneUserQuery
from user.application.queries.find_one.types.dto import FindOneUserDto
from user.application.commands.update.types import dto
from user.application.info.current_user_found_info import current_user_info
from user.infrastructure.repositories.postgres.sqlalchemy.user_repository import (
    UserRepositorySqlAlchemy,
)
from user.infrastructure.routes.types.create.create_user_dto import CreateUserDto
from user.infrastructure.routes.types.login.login_dto import LoginDto
from user.infrastructure.routes.types.login.login_response import Token
from user.infrastructure.routes.types.update.update_user_dto import UpdateUserDto
from user.application.errors.not_found import user_not_found_error

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("")
async def create_user(
    body: CreateUserDto,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
    
):
    result = await command_bus.dispatch(body)
    return result

@user_router.get("/one/{id}")
async def find_one_user(
        id: UUID4,
        _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN, AuthUserRole.MANAGER]))],
        session=Depends(get_mongo_client),
    ):

    db = session["template"]
    user_coll = db["user"]
    user = user_coll.find_one({"id": str(id)})
    
    if is_none(user):
        error = user_not_found_error()
        raise error_response_handler(error) 
    
    user_response =  {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "role": user["role"],
            "status": user["status"],
        }
    
    return success_response_handler(
        user_response,
        user_found_info()
    )

@user_router.get("/managers")
async def find_all_managers(_: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))], session=Depends(get_session)):
    result = await ErrorDecorator(
        service= FindAllManagersQuery(user_repository=UserRepositorySqlAlchemy(session)),
        error_handler=error_response_handler,
    ).execute(data= None)
    
    return result.handle_success(handler=success_response_handler)

@user_router.patch("")
async def update_user(
    body: UpdateUserDto,
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    session= Depends(get_session),
    cryptography_provider= Depends(get_fernet_provider)
):
    if current_user.role.name != UserRole.ADMIN.name: #? Un Manager podría actualizar los permisos de un usuario?
        if (current_user.id != body.id) or (is_not_none(body.role) and (body.role.name != UserRole.CLIENT.name)):
            raise HTTPException( 
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="You don't have enough permissions",
            )

    result = await ErrorDecorator(
        service= UpdateUserCommand(
            user_repository= UserRepositorySqlAlchemy(session),
            cryptography_provider= cryptography_provider
        ),
        error_handler= error_response_handler
    ).execute(data= dto.UpdateUserDto(
        id= body.id,
        username= body.username,
        email= body.email,
        password= body.password,
        first_name= body.first_name,
        last_name= body.last_name,
        current_role= UserRole.CLIENT,
        new_role= body.role,
        status= body.status
    ))

    return result.handle_success(handler= success_response_handler)
    
@user_router.patch("/manager")
async def update_manager(
    body: UpdateUserDto,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))], 
    session= Depends(get_session),
    cryptography_provider= Depends(get_fernet_provider)       
):
    result = await ErrorDecorator(
        service= UpdateUserCommand(
            user_repository= UserRepositorySqlAlchemy(session),
            cryptography_provider= cryptography_provider
        ),
        error_handler= error_response_handler
    ).execute(data= dto.UpdateUserDto(
        id= body.id,
        username= body.username,
        email= body.email,
        password= body.password,
        first_name= body.first_name,
        last_name= body.last_name,
        current_role= UserRole.MANAGER,
        new_role= body.role,
        status= body.status
    ))

    return result.handle_success(handler= success_response_handler)

@user_router.delete("/managers/{id}")
async def delete_manager(
    id: UUID4,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
    session = Depends(get_session)
):
    result = await ErrorDecorator(
        service= DeleteManagerCommand(
            user_repository= UserRepositorySqlAlchemy(session)
        ),
        error_handler= error_response_handler
    ).execute(data= DeleteManagerDto(str(id)))

    return result.handle_success(handler= success_response_handler)


@user_router.post("/login")
async def login(
    userdetails: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session),
    token_provider=Depends(get_jwt_provider),
    cryptography_provider=Depends(get_fernet_provider),
):

    dto = LoginDto(login_credential=userdetails.username, password=userdetails.password)

    result = await ErrorDecorator(
        service=LoginCommand(
            user_repository=UserRepositorySqlAlchemy(session),
            token_provider=token_provider,
            cryptography_provider=cryptography_provider,
        ),
        error_handler=error_response_handler,
    ).execute(data=dto)

    return Token(access_token=result.unwrap().token, token_type="bearer")


@user_router.get("/me")
async def current(user: Annotated[AuthUser, Depends(get_current_user)]):

    result = Result.success(user, current_user_info())

    return result.handle_success(handler=success_response_handler)

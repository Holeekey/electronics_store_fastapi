from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from pymongo import MongoClient

from common.application.decorators.error_decorator import ErrorDecorator
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from common.infrastructure.auth.get_current_user import get_current_user
from common.infrastructure.auth.models.auth_user import AuthUser, AuthUserRole
from common.infrastructure.auth.role_checker import role_checker
from common.infrastructure.bus.bus import Bus, get_command_bus
from common.infrastructure.database.database import get_session
from common.infrastructure.database.mongo import get_mongo_client
from common.infrastructure.pagination.pagination_params import pagination_params
from common.infrastructure.pagination.utils.pagination_to_skip import pagination_to_skip
from common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from common.infrastructure.responses.handlers.pagination_response_handler import pagination_response_handler
from common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from common.infrastructure.responses.pagination_response import PaginationInfo
from common.infrastructure.token.jwt.jwt_provider import get_jwt_provider
from common.infrastructure.cryptography.fernet_cryptography_provider import get_fernet_provider
from user.application.commands.delete_manager.types.dto import DeleteManagerDto
from user.application.commands.login.login_command import LoginCommand
from user.application.info.many_users_found_info import many_users_found_info
from user.application.info.user_found_info import user_found_info
from user.application.models.user import UserRole
from user.application.info.current_user_found_info import current_user_info
from user.infrastructure.repositories.postgres.sqlalchemy.user_repository import (
    UserRepositorySqlAlchemy,
)
from user.infrastructure.routes.types.create.create_user_dto import CreateUserDto
from user.infrastructure.routes.types.login.login_dto import LoginDto
from user.infrastructure.routes.types.login.login_response import Token
from user.infrastructure.routes.types.update.update_user_dto import UpdateUserDto
from user.application.commands.update.types.dto import UpdateUserDto as UpdateUserDtoApp
from user.application.errors.not_found import user_not_found_error

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("")
async def create_user(
    body: CreateUserDto,
    # _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
    
):
    result = await command_bus.dispatch(body)
    return result

@user_router.patch("")
async def update_user(
    body: UpdateUserDto,
    #_: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
):
    result = await command_bus.dispatch(UpdateUserDtoApp(
        id=body.id,
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password=body.password,
        username=body.username,
        status=body.status,
        role_to_update=None
    ))
    return result
    
@user_router.patch("/manager")
async def update_manager(
    body: UpdateUserDto,
    #_: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))], 
    command_bus: Annotated[Bus, Depends(get_command_bus)],   
):
    result = await command_bus.dispatch(UpdateUserDtoApp(
        id=body.id,
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password=body.password,
        username=body.username,
        status=body.status,
        role_to_update=UserRole.MANAGER,
    ))
    return result

@user_router.delete("/managers/{id}")
async def delete_manager(
    id: UUID4,
    # _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
):
    result = await command_bus.dispatch(DeleteManagerDto(str(id)))
    return result

@user_router.get("/one/{id}")
async def find_one_user(
        id: UUID4,
        # _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN, AuthUserRole.MANAGER]))],
        session: Annotated[MongoClient,Depends(get_mongo_client)],
    ):

    db = session["template"]
    user_coll = db["user"]
    
    projection = {
        "_id": 0,
    }
    
    user = user_coll.find_one({"id": str(id)},projection)
    
    if is_none(user):
        error = user_not_found_error()
        raise error_response_handler(error) 
    
    return success_response_handler(
        user,
        user_found_info()
    )

@user_router.get("/managers")
async def find_all_managers(
        # _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
        session: Annotated[MongoClient,Depends(get_mongo_client)],
        pagination: Annotated[dict, Depends(pagination_params)]
    ):
    db = session["template"]
    user_coll = db["user"]
    
    projection = {
        "_id": 0,
    }
    
    where = {"role": "MANAGER"}
        
    users_cursor = user_coll.find(where, projection).skip(pagination_to_skip(pagination)).limit(pagination["per_page"])
    total_count = user_coll.count_documents(where)
    users = list(users_cursor)
    pagination_info = PaginationInfo.make_pagination_info(pagination["page"], pagination["per_page"], total_count)
    
    return pagination_response_handler(t=users, info=many_users_found_info(), pagination_info=pagination_info)

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

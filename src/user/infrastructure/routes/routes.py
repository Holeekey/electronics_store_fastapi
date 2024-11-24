from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4

from common.application.decorators.error_decorator import ErrorDecorator
from common.domain.result.result import Result
from common.infrastructure.auth.get_current_user import get_current_user
from common.infrastructure.auth.models.auth_user import AuthUser, AuthUserRole
from common.infrastructure.auth.role_checker import role_checker
from common.infrastructure.database.database import get_session
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from common.infrastructure.token.jwt.jwt_provider import get_jwt_provider
from user.application.commands.create.create_user_command import CreateUserCommand
from user.application.commands.login.login_command import LoginCommand
from user.application.queries.find_one.find_one_user_query import FindOneUserQuery
from user.application.queries.find_one.types.dto import FindOneUserDto
from user.application.info.current_user_found_info import current_user_info
from user.infrastructure.repositories.postgres.sqlalchemy.user_repository import (
    UserRepositorySqlAlchemy,
)
from user.infrastructure.routes.types.create.create_user_dto import CreateUserDto
from user.infrastructure.routes.types.login.login_dto import LoginDto
from user.infrastructure.routes.types.login.login_response import Token


user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/one/{id}")
async def find_one_user(id: UUID4, session=Depends(get_session)):

    result = await ErrorDecorator(
        service=FindOneUserQuery(user_repository=UserRepositorySqlAlchemy(session)),
        error_handler=error_response_handler,
    ).execute(data=FindOneUserDto(id=id.__str__()))

    return result.handle_success(handler=success_response_handler)


@user_router.post("")
async def create_user(
    body: CreateUserDto,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
    session=Depends(get_session),
):

    idGenerator = UUIDGenerator()

    result = await ErrorDecorator(
        service=CreateUserCommand(
            id_generator=idGenerator, user_repository=UserRepositorySqlAlchemy(session)
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)


@user_router.post("/login")
async def login(
    userdetails: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session),
    token_provider=Depends(get_jwt_provider),
):

    dto = LoginDto(login_credential=userdetails.username, password=userdetails.password)

    result = await ErrorDecorator(
        service=LoginCommand(
            user_repository=UserRepositorySqlAlchemy(session),
            token_provider=token_provider,
        ),
        error_handler=error_response_handler,
    ).execute(data=dto)

    return Token(access_token=result.unwrap().token, token_type="bearer")


@user_router.get("/me")
async def current(user: Annotated[AuthUser, Depends(get_current_user)]):

    result = Result.success(user, current_user_info())

    return result.handle_success(handler=success_response_handler)

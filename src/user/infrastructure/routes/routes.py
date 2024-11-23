from fastapi import APIRouter, Depends
from pydantic import UUID4

from common.application.decorators.error_decorator import ErrorDecorator
from common.infrastructure.database.database import get_session
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from user.application.commands.create.create_user_command import CreateUserCommand
from user.application.queries.find_one.find_one_user_query import FindOneUserQuery
from user.application.queries.find_one.types.dto import FindOneUserDto
from user.infrastructure.repositories.postgres.sqlalchemy.user_repository import (
    UserRepositorySqlAlchemy,
)
from user.infrastructure.routes.types.dto.create.create_user_dto import CreateUserDto


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
async def create_user(body: CreateUserDto, session=Depends(get_session)):

    # idGenerator = RandomIdGenerator()
    idGenerator = UUIDGenerator()

    result = await ErrorDecorator(
        service=CreateUserCommand(
            id_generator=idGenerator, user_repository=UserRepositorySqlAlchemy(session)
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)

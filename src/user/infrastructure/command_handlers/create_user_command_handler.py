from common.application.decorators.error_decorator import ErrorDecorator
from common.application.decorators.logger_decorator import LoggerDecorator
from common.infrastructure.cryptography.fernetCryptography_provider import get_fernet_provider
from common.infrastructure.database.database import get_session
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.loggers.loguru_logger import LoguruLogger
from common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from user.application.commands.create.create_user_command import CreateUserCommand
from user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy
from user.infrastructure.routes.types.create.create_user_dto import CreateUserDto


async def create_user_command_handler(
    body: CreateUserDto,
    session=get_session().__next__(),
):
    idGenerator = UUIDGenerator()  
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service= CreateUserCommand(
                user_repository= UserRepositorySqlAlchemy(session),
                id_generator= idGenerator,
                cryptography_provider= get_fernet_provider()
            ),
            loggers = [LoguruLogger("Create User")]
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)
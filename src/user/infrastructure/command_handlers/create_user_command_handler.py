from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.cryptography.fernet.fernet_cryptography_provider import get_fernet_provider
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from src.user.application.commands.create.create_user_command import CreateUserCommand
from src.user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy
from src.user.infrastructure.routes.types.create.create_user_dto import CreateUserDto


async def create_user_command_handler(
    body: CreateUserDto,
):
    idGenerator = UUIDGenerator()  
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service= CreateUserCommand(
                user_repository= UserRepositorySqlAlchemy(get_session().__next__()),
                id_generator= idGenerator,
                cryptography_provider= get_fernet_provider(),
                event_publisher= await get_rabbit_mq_event_publisher().__anext__(),
            ),
            loggers = [LoguruLogger("Create User")]
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)
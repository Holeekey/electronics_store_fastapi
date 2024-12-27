from common.application.decorators.error_decorator import ErrorDecorator
from common.application.decorators.logger_decorator import LoggerDecorator
from common.infrastructure.cryptography.fernet_cryptography_provider import get_fernet_provider
from common.infrastructure.database.database import get_session
from common.infrastructure.loggers.loguru_logger import LoguruLogger
from common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from common.infrastructure.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from user.application.commands.update.update_user_command import UpdateUserCommand
from user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy
from user.infrastructure.repositories.postgres.sqlalchemy.manager_repository import ManagerRepositorySqlAlchemy
from user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy
from user.application.commands.update.update_user_command import UpdateUserDto


async def update_user_command_handler(
    body: UpdateUserDto,
):
    
    db = get_session().__next__()
    
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service= UpdateUserCommand(
                user_repository= UserRepositorySqlAlchemy(db),
                manager_repository= ManagerRepositorySqlAlchemy(db),
                client_repository= ClientRepositorySqlAlchemy(db),
                cryptography_provider= get_fernet_provider(),
                event_publisher= await get_rabbit_mq_event_publisher().__anext__(),
            ),
            loggers = [LoguruLogger("Update User")]
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)
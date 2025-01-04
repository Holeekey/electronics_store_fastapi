from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.cryptography.fernet.fernet_cryptography_provider import get_fernet_provider
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from src.user.application.commands.delete_manager.delete_manager_command import DeleteManagerCommand
from src.user.application.commands.delete_manager.types.dto import DeleteManagerDto
from src.user.application.commands.update.update_user_command import UpdateUserCommand
from src.user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.manager_repository import ManagerRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy
from src.user.application.commands.update.update_user_command import UpdateUserDto


async def delete_manager_command_handler(
    body: DeleteManagerDto,
):
    
    db = get_session().__next__()
    
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service= DeleteManagerCommand(
                user_repository= UserRepositorySqlAlchemy(db),
                manager_repository= ManagerRepositorySqlAlchemy(db),
                event_publisher= await get_rabbit_mq_event_publisher().__anext__(),
            ),
            loggers = [LoguruLogger("Delete Manager")]
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)
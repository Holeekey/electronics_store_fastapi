from uuid import UUID

from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher

from src.product.application.commands.delete.delete_product_command import DeleteProductCommand
from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import ProductRepositorySqlAlchemy
from src.product.infrastructure.routes.types.delete_product_dto import DeleteProductDto

async def delete_product_command_handler(
    data: DeleteProductDto,
):
    
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service= DeleteProductCommand(
                product_repository= ProductRepositorySqlAlchemy(get_session().__next__()),
                publisher= await get_rabbit_mq_event_publisher().__anext__(),
            ),
            loggers = [LoguruLogger("Delete Product")]
        ),
        error_handler=error_response_handler,
    ).execute(data=data)

    return result.handle_success(handler=success_response_handler)
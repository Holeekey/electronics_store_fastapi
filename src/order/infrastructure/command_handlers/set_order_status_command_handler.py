from src.order.application.services.set_status.set_order_status_service import SetOrderStatusService
from src.order.application.services.set_status.types.dto import SetOrderStatusDto
from src.order.infrastructure.repositories.postgres.sqlalchemy.order_repository import OrderRepositorySqlAlchemy
from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler

async def set_order_status_command_handler(
    command: SetOrderStatusDto
):
    session = get_session().__next__()
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service=SetOrderStatusService(
                order_repository= OrderRepositorySqlAlchemy(session),
                event_publisher= await get_rabbit_mq_event_publisher().__anext__(),
                
            ),
            loggers= [LoguruLogger("Set Order Status")]
        ),
        error_handler=error_response_handler,
    ).execute(data=command)
    
    return result.handle_success(handler=success_response_handler)
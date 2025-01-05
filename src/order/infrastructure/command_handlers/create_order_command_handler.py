from src.order.application.services.create.create_order_service import CreateOrderService
from src.order.application.services.create.types.dto import CreateOrderDto
from src.order.domain.services.create_order_domain_service import CreateOrderDomainService
from src.order.infrastructure.repositories.postgres.sqlalchemy.order_repository import OrderRepositorySqlAlchemy
from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import ProductRepositorySqlAlchemy
from src.shopping_cart.infrastructure.repositories.postgres.sqlalchemy.shopping_cart_repository import ShoppingCartRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy

async def create_order_command_handler(
    command: CreateOrderDto
):
    session = get_session().__next__()
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service=CreateOrderService(
                order_repository= OrderRepositorySqlAlchemy(session),
                client_repository= ClientRepositorySqlAlchemy(session),
                create_order_service= CreateOrderDomainService(ProductRepositorySqlAlchemy(session)),
                shopping_cart_repository= ShoppingCartRepositorySqlAlchemy(session),
                event_publisher= await get_rabbit_mq_event_publisher().__anext__(),
                
            ),
            loggers= [LoguruLogger("Create Order")]
        ),
        error_handler=error_response_handler,
    ).execute(data=command)
    
    return result.handle_success(handler=success_response_handler)
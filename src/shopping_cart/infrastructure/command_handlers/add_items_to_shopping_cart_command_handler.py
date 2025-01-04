from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from src.common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import ProductRepositorySqlAlchemy
from src.shopping_cart.application.services.add_items.add_items_to_shopping_cart_service import AddItemsToShoppingCartService
from src.shopping_cart.infrastructure.repositories.postgres.sqlalchemy.shopping_cart_repository import ShoppingCartRepositorySqlAlchemy
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartCommand
from src.user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy

async def add_items_to_shopping_cart_command_handler(
    command: AddItemsToShoppingCartCommand
):
    session = get_session().__next__()
    id_generator = UUIDGenerator()
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service=AddItemsToShoppingCartService(
                id_generator=id_generator,
                client_repository= ClientRepositorySqlAlchemy(session),
                product_repository= ProductRepositorySqlAlchemy(),
                shopping_cart_repository= ShoppingCartRepositorySqlAlchemy(session),
                event_publisher= await get_rabbit_mq_event_publisher().__anext__()
            ),
            loggers= [LoguruLogger("Add Items to Shopping Cart")]
        ),
        error_handler=error_response_handler,
    ).execute(data=command)
    
    return result.handle_success(handler=success_response_handler)
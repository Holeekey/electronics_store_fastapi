from src.shopping_cart.application.services.remove_item.remove_item_from_shopping_cart_service import RemoveItemFromShoppingCartService
from src.shopping_cart.application.services.remove_item.types.dto import RemoveItemFromShoppingCartDto
from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.shopping_cart.infrastructure.repositories.postgres.sqlalchemy.shopping_cart_repository import ShoppingCartRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy

async def remove_item_from_shopping_cart_command_handler(
    command: RemoveItemFromShoppingCartDto
):
    session = get_session().__next__()
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service=RemoveItemFromShoppingCartService(
                client_repository= ClientRepositorySqlAlchemy(session),
                shopping_cart_repository= ShoppingCartRepositorySqlAlchemy(session),
                event_publisher= await get_rabbit_mq_event_publisher().__anext__()
            ),
            loggers= [LoguruLogger("Remove Item From Shopping Cart")]
        ),
        error_handler=error_response_handler,
    ).execute(data=command)
    
    return result.handle_success(handler=success_response_handler)
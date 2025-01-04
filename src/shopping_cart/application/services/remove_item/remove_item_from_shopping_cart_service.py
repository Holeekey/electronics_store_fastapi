from dataclasses import dataclass
from uuid import UUID
from src.common.application.events.event_handlers import IEventPublisher
from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result
from src.common.domain.utils.is_none import is_none
from src.product.domain.value_objects.product_id import ProductId
from src.shopping_cart.application.info.remove_item_from_shopping_cart_info import remove_item_from_shopping_cart_info
from src.shopping_cart.application.errors.client_shopping_cart_does_not_includes_product import client_shopping_cart_does_not_includes_product_error
from src.shopping_cart.application.repositories.shopping_cart_repository import IShoppingCartRepository
from src.shopping_cart.application.services.remove_item.types.dto import RemoveItemFromShoppingCartDto
from src.shopping_cart.application.services.remove_item.types.response import RemoveItemFromShoppingCartResponse
from src.shopping_cart.application.errors.client_not_found import client_not_found_error
from src.user.application.repositories.client_repository import IClientRepository
from src.user.domain.client.value_objects.client_id import ClientId


@dataclass
class RemoveItemFromShoppingCartService(IApplicationService):
    
    client_repository: IClientRepository
    shopping_cart_repository: IShoppingCartRepository
    event_publisher: IEventPublisher
    
    async def execute(self, data: RemoveItemFromShoppingCartDto) -> Result[RemoveItemFromShoppingCartResponse]:
        
        client_id = ClientId(UUID(data.client_id))

        client = await self.client_repository.find_one(client_id)

        if is_none(client):
            return Result.failure(client_not_found_error())

        shopping_cart = await self.shopping_cart_repository.find_by_client_id(client_id)
        
        product_id = ProductId(data.product_id)
        
        if is_none(shopping_cart) or shopping_cart.has_item(product_id) is False:
            return Result.failure(client_shopping_cart_does_not_includes_product_error())
        
        shopping_cart.remove_item(product_id)
        
        await self.shopping_cart_repository.save(shopping_cart)

        await self.event_publisher.publish(shopping_cart.pull_events())

        return Result.success(RemoveItemFromShoppingCartResponse('Succesful'), remove_item_from_shopping_cart_info())
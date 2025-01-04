

from dataclasses import dataclass
from uuid import UUID
from common.application.events.event_handlers import IEventPublisher
from common.application.id_generator.id_generator import IDGenerator
from common.application.service.application_service import IApplicationService
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from order.application.errors.client_not_found import client_not_found_error
from order.application.errors.shopping_cart_empty import shopping_cart_empty_error
from order.application.repositories.order_repository import IOrderRepository
from order.application.services.create.types.dto import CreateOrderDto
from order.application.services.create.types.response import CreateOrderReponse
from product.application.repositories.product_repository import IProductRepository
from shopping_cart.application.repositories.shopping_cart_repository import IShoppingCartRepository
from user.application.repositories.client_repository import IClientRepository
from user.domain.client.value_objects.client_id import ClientId


@dataclass
class CreateOrderService(IApplicationService):
    
    id_generator: IDGenerator
    order_repository: IOrderRepository
    client_repository: IClientRepository
    product_repository: IProductRepository
    shopping_cart_repository: IShoppingCartRepository
    event_publisher: IEventPublisher
    
    async def execute(self, data: CreateOrderDto) -> Result[CreateOrderReponse]:
        
        client_id = ClientId(UUID(data.client_id))
        
        client = await self.client_repository.find_one(client_id)
        
        if is_none(client):
            Result.failure(client_not_found_error())
            
        shopping_cart = await self.shopping_cart_repository.find_by_client_id(client_id)
        
        if is_none(shopping_cart) or not len(shopping_cart.items) > 0:
            Result.failure(shopping_cart_empty_error())
            
        
            
        
         
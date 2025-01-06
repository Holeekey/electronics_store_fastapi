

from dataclasses import dataclass
from uuid import UUID
from order.application.errors.not_enough_stock import not_enough_stock_error
from src.inventory.application.repositories.inventory_repository import IInventoryRepository
from src.common.domain.utils.is_not_none import is_not_none
from src.common.application.events.event_handlers import IEventPublisher
from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result
from src.common.domain.utils.is_none import is_none
from src.order.application.errors.client_not_found import client_not_found_error
from src.order.application.errors.shopping_cart_empty import shopping_cart_empty_error
from src.order.application.info.create_order_info import create_order_info
from src.order.application.repositories.order_repository import IOrderRepository
from src.order.application.services.create.types.dto import CreateOrderDto
from src.order.application.services.create.types.response import CreateOrderReponse
from src.order.domain.services.create_order_domain_service import CreateOrderDomainService
from src.inventory.domain.value_objects.inventory_stock import Stock
from src.shopping_cart.application.repositories.shopping_cart_repository import IShoppingCartRepository
from src.user.application.repositories.client_repository import IClientRepository
from src.user.domain.client.value_objects.client_id import ClientId


@dataclass
class CreateOrderService(IApplicationService):
    
    order_repository: IOrderRepository
    client_repository: IClientRepository
    shopping_cart_repository: IShoppingCartRepository
    create_order_service: CreateOrderDomainService
    inventory_repository: IInventoryRepository
    event_publisher: IEventPublisher
    
    async def execute(self, data: CreateOrderDto) -> Result[CreateOrderReponse]:
        
        client_id = ClientId(UUID(data.client_id))
        
        client = await self.client_repository.find_one(client_id)
        
        if is_none(client):
            Result.failure(client_not_found_error())
            
        shopping_cart = await self.shopping_cart_repository.find_by_client_id(client_id)
        
        if is_none(shopping_cart) or len(shopping_cart.items) == 0:
            return Result.failure(shopping_cart_empty_error())
        
        inventories_to_update = []
        
        for item in shopping_cart.items:
            inventory = await self.inventory_repository.find_by_product_id(item.product_id)
            
            if is_none(inventory) or inventory.stock.value < item.quantity.value:
                return Result.failure(not_enough_stock_error())
            
            inventory.stock = Stock(inventory.stock.value - item.quantity.value)
            
            inventories_to_update.append(inventory)
            
            
        order = await self.create_order_service.create(shopping_cart)
            
        shopping_cart.clear_items()
        
        await self.shopping_cart_repository.save(shopping_cart)
        
        await self.order_repository.save(order)
        
        for inventory in inventories_to_update:
            await self.inventory_repository.save(inventories_to_update)
        
        await self.event_publisher.publish(order.pull_events())
        await self.event_publisher.publish(shopping_cart.pull_events())
        
        return Result.success(CreateOrderReponse(order_id=order.id.id),create_order_info())
            
        
         
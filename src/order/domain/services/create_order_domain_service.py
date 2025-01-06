

from dataclasses import dataclass
from datetime import datetime
import uuid
from src.order.domain.entities.order_item import OrderItem
from src.order.domain.order import Order
from src.order.domain.value_objects.order_creation_date import OrderCreationDate
from src.order.domain.value_objects.order_id import OrderId
from src.order.domain.value_objects.order_item_id import OrderItemId
from src.order.domain.value_objects.order_item_price import OrderItemPrice
from src.order.domain.value_objects.order_item_quantity import OrderItemQuantity
from src.order.domain.value_objects.order_status import OrderStatus, OrderStatusOptions
from src.shopping_cart.domain.shopping_cart import ShoppingCart
from src.product.application.repositories.product_repository import IProductRepository
@dataclass
class CreateOrderDomainService():
    
    product_repository: IProductRepository
    
    async def create(self, shopping_cart: ShoppingCart)-> Order:
        
        return Order(
            id = OrderId(uuid.uuid4()),
            client_id= shopping_cart.client_id,
            creation_date= OrderCreationDate(datetime.now()),
            status= OrderStatus(OrderStatusOptions.PENDING),
            items= [
                OrderItem(
                    id= OrderItemId(uuid.uuid4()),
                    quantity= OrderItemQuantity(item.quantity.quantity),
                    product_id= item.product_id,
                    product_price= OrderItemPrice((await self.product_repository.find_one(item.product_id)).pricing.price)
                )
                for item in shopping_cart.items
            ]
        )
        
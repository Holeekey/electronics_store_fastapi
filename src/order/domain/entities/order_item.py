from typing import TypeVar

from order.domain.value_objects.order_item_price import OrderItemPrice
from src.order.domain.value_objects.order_item_quantity import OrderItemQuantity
from src.product.domain.value_objects.product_id import ProductId
from src.common.domain.entity.entity import Entity
from src.order.domain.value_objects.order_item_id import OrderItemId


T = TypeVar("T", bound=OrderItemId)


class OrderItem(Entity[T]):
    def __init__(
        self,
        id: OrderItemId,
        product_id:ProductId,
        quantity: OrderItemQuantity,
        price: OrderItemPrice,
    ):
        super().__init__(id)
        self._product_id = product_id
        self._quantity = quantity
        self._price = price
    
    @property
    def quantity(self) -> OrderItemQuantity:
        return self._quantity
    
    @property
    def product_id(self) -> ProductId:
        return self._product_id
    
    @property
    def product_price(self) -> OrderItemPrice:
        return self._price
        
    def __eq__(self, other: 'OrderItem') -> bool:
        return self._id == other.id
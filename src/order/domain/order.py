from typing import TypeVar

from src.order.domain.events.order_cancelled import OrderCancelled
from src.order.domain.events.order_completed import OrderCompleted
from src.order.domain.errors.order_is_not_cancelable import order_is_not_cancelable_error
from src.order.domain.errors.order_is_not_completable import order_is_not_completable_error
from src.order.domain.entities.order_item import OrderItem
from src.order.domain.events.order_created import OrderCreated
from src.order.domain.value_objects.order_status import OrderStatus, OrderStatusOptions
from src.order.domain.value_objects.order_creation_date import OrderCreationDate
from src.common.domain.aggregate.aggregate import Aggregate
from src.order.domain.value_objects.order_id import OrderId
from src.user.domain.client.value_objects.client_id import ClientId


T = TypeVar("T", bound=OrderId)


class Order(Aggregate[T]):
    def __init__(
        self,
        id: OrderId,
        client_id: ClientId,
        creation_date: OrderCreationDate,
        items: list[OrderItem],
        status: OrderStatus = OrderStatus(OrderStatusOptions.PENDING)
    ) -> None:
        super().__init__(id)
        self._client_id = client_id
        self._creation_date = creation_date
        self._items = items
        self._status = status
        self.publish(OrderCreated(
            order_id=id,
            client_id=client_id,
            creation_date=creation_date,
            items=items
        ))
    
    @property
    def status(self) -> OrderStatus:
        return self._status
    
    def complete(self):
        if not self._status.is_completable():
            raise order_is_not_completable_error()
        self._status = OrderStatus(OrderStatusOptions.COMPLETED)
        self.publish(OrderCompleted(self._id))
        
    def cancel(self):
        if not self._status.is_cancelable():
            raise order_is_not_cancelable_error()
        self._status = OrderStatus(OrderStatusOptions.CANCELLED)
        self.publish(OrderCancelled(self._id))
        
    def get_total_price(self) -> float:
        return sum([item.product_price.price for item in self._items])
    
    def validate_state(self) -> None:
        self._id.validate()
        self._client_id.validate()
        self._creation_date.validate()
        for item in self._items:
            item._id.validate()
            item.product_id.validate()
            item.product_price.validate()
            item.quantity.validate()
        
        
    

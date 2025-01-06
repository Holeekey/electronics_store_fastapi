from src.order.domain.entities.order_item import OrderItem
from src.order.domain.value_objects.order_creation_date import OrderCreationDate
from src.order.domain.value_objects.order_id import OrderId
from src.common.domain.events.domain_event import DomainEvent
from src.user.domain.client.value_objects.client_id import ClientId

ORDER_CANCELLED = "order_cancelled"


class OrderCancelled(DomainEvent):
    def __init__(
        self, 
        order_id: OrderId,
    ):
        super().__init__(ORDER_CANCELLED)
        self.order_id = order_id
        

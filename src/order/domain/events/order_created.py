from src.order.domain.entities.order_item import OrderItem
from src.order.domain.value_objects.order_creation_date import OrderCreationDate
from src.order.domain.value_objects.order_id import OrderId
from src.common.domain.events.domain_event import DomainEvent
from src.user.domain.client.value_objects.client_id import ClientId

ORDER_CREATED = "order_created"


class OrderCreated(DomainEvent):
    def __init__(
        self, 
        order_id: OrderId,
        client_id: ClientId,
        creation_date: OrderCreationDate,
        items: list[OrderItem]
    ):
        super().__init__(ORDER_CREATED)
        self.order_id = order_id
        self.client_id = client_id
        self.creation_date = creation_date
        self.items = items
        

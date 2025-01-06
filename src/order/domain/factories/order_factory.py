
from datetime import datetime
from uuid import UUID
from src.order.domain.entities.order_item import OrderItem
from src.order.domain.order import Order
from src.order.domain.value_objects.order_creation_date import OrderCreationDate
from src.order.domain.value_objects.order_id import OrderId
from src.order.domain.value_objects.order_status import OrderStatus, OrderStatusOptions
from src.user.domain.client.value_objects.client_id import ClientId


def order_factory(
    id: UUID,
    client_id: UUID,
    creation_date: datetime,
    status: OrderStatusOptions,
    items: list[OrderItem],
):
    return Order(
        id=OrderId(id),
        client_id=ClientId(client_id),
        creation_date=OrderCreationDate(creation_date),
        status=OrderStatus(status),
        items= items,
    )
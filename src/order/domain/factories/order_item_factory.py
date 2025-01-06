
from uuid import UUID
from src.order.domain.entities.order_item import OrderItem
from src.order.domain.value_objects.order_item_id import OrderItemId
from src.order.domain.value_objects.order_item_price import OrderItemPrice
from src.order.domain.value_objects.order_item_quantity import OrderItemQuantity
from src.product.domain.value_objects.product_id import ProductId


def order_item_factory(
    id: UUID,
    product_id: str,
    quantity: int,
    product_price: float,
):
    return OrderItem(
        id=OrderItemId(id),
        product_id=ProductId(product_id),
        quantity=OrderItemQuantity(quantity),
        product_price=OrderItemPrice(product_price)
    )
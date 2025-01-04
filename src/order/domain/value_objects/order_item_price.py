from src.common.domain.value_object.value_object import ValueObject
from src.order.domain.errors.invalid_order_item_price import invalid_order_item_price_error


class OrderItemPrice(ValueObject):
    def __init__(self, price: float) -> None:
        self.value = id
        self.validate()

    @property
    def price(self) -> float:
        return self.value

    def validate(self) -> None:
        if self.value < 0.00:
            raise invalid_order_item_price_error()

    def __eq__(self, other: "OrderItemPrice") -> bool:
        return self.value == other.id
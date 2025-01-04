from src.common.domain.value_object.value_object import ValueObject
from src.order.domain.errors.invalid_order_item_quantity import invalid_order_item_quantity_error


class OrderItemQuantity(ValueObject):
    def __init__(self, quantity: int) -> None:
        self.value = quantity
        self.validate()

    @property
    def quantity(self) -> int:
        return self.value

    def validate(self) -> None:
        if not self.value > 0:
            raise invalid_order_item_quantity_error()

    def __eq__(self, other: "OrderItemQuantity") -> bool:
        return self.value == other.quantity
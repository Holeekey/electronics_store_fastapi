from uuid import UUID
from src.common.domain.value_object.value_object import ValueObject
from src.shopping_cart.domain.errors.invalid_shopping_cart_item_quantity import invalid_shopping_cart_item_quantity_error


class ShoppingCartItemQuantity(ValueObject):
    def __init__(self, quantity: int) -> None:
        self.value = quantity
        self.validate()

    @property
    def quantity(self) -> int:
        return self.value

    def validate(self) -> None:
        if not self.value > 0:
            raise invalid_shopping_cart_item_quantity_error()

    def __eq__(self, other: "ShoppingCartItemQuantity") -> bool:
        return self.value == other.quantity
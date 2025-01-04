from uuid import UUID
from src.common.domain.value_object.value_object import ValueObject
from src.shopping_cart.domain.errors.invalid_shopping_cart_id import invalid_shopping_cart_id_error


class ShoppingCartId(ValueObject):
    def __init__(self, id: UUID) -> None:
        self.value = id
        self.validate()

    @property
    def id(self) -> UUID:
        return self.value

    def validate(self) -> None:
        if not isinstance(self.id, UUID):
            raise invalid_shopping_cart_id_error()

    def __eq__(self, other: "ShoppingCartId") -> bool:
        return self.value == other.id
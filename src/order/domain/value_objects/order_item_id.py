from uuid import UUID
from src.common.domain.value_object.value_object import ValueObject
from src.order.domain.errors.invalid_order_item_id import invalid_order_item_id_error


class OrderItemId(ValueObject):
    def __init__(self, id: UUID) -> None:
        self.value = id
        self.validate()

    @property
    def id(self) -> UUID:
        return self.value

    def validate(self) -> None:
        if not isinstance(self.id, UUID):
            raise invalid_order_item_id_error()

    def __eq__(self, other: "OrderItemId") -> bool:
        return self.value == other.id
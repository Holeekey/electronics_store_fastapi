from uuid import UUID
from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_product_id import invalid_product_id_error


class ProductId(ValueObject):
    def __init__(self, id: str) -> None:
        self.value = id
        self.validate()

    @property
    def id(self) -> str:
        return self.value

    def validate(self) -> None:
        try:
            UUID(self.id)
        except:
            raise invalid_product_id_error()

    def __eq__(self, other: "ProductId") -> bool:
        return self.value == other.id

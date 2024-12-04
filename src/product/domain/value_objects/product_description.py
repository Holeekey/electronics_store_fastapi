from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_product_description import invalid_product_description_error


class ProductDescription(ValueObject):
    def __init__(self, description: str) -> None:
        self.value = description
        self.validate()

    @property
    def description(self) -> str:
        return self.value

    def validate(self) -> None:
        if self.description is None:
            raise invalid_product_description_error()

    def __eq__(self, other: "ProductDescription") -> bool:
        return self.description == other.description

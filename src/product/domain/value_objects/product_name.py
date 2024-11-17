from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_product_name import invalid_product_name_error


class ProductName(ValueObject):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.validate()

    @property
    def name(self) -> str:
        return self.value

    def validate(self) -> None:
        if len(self.name) < 3:
            raise invalid_product_name_error()

    def __eq__(self, other: "ProductName") -> bool:
        return self.name == other.name
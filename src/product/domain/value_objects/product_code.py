from src.common.domain.value_object.value_object import ValueObject
from src.product.domain.errors.invalid_product_code import invalid_product_code_error


class ProductCode(ValueObject):
    def __init__(self, code: str) -> None:
        self.value = code
        self.validate()

    @property
    def code(self) -> str:
        return self.value

    def validate(self) -> None:
        if len(self.code) == 0:
            raise invalid_product_code_error()

    def __eq__(self, other: "ProductCode") -> bool:
        return self.code == other.code

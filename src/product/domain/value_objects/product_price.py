from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_product_price import invalid_product_price_error


class ProductPrice(ValueObject):
    def __init__(self, price: float) -> None:
        self.value = price
        self.validate()

    @property
    def price(self) -> float:
        return self.value

    def validate(self) -> None:
        if self.price < 0:
            raise invalid_product_price_error()

    def __eq__(self, other: "ProductPrice") -> bool:
        return self.price == other.price

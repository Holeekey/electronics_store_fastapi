from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_inventory_stock import invalid_inventory_stock_error


class Stock(ValueObject):
    def __init__(self, stock: int) -> None:
        self.value = stock
        self.validate()

    @property
    def price(self) -> int:
        return self.value

    def validate(self) -> None:
        if self.price < 0:
            raise invalid_inventory_stock_error()

    def __eq__(self, other: "Stock") -> bool:
        return self.stock == other.price

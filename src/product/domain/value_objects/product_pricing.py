from src.common.domain.value_object.value_object import ValueObject
from src.product.domain.errors.invalid_product_price import invalid_product_price_error
from src.product.domain.errors.invalid_product_margin import invalid_product_price_margin_error
from src.product.domain.errors.invalid_product_cost import invalid_product_cost_error


class ProductPricing(ValueObject):
    def __init__(self, cost: float, margin: float) -> None:
        
        if (margin >= 1) or (margin < 0):
            raise invalid_product_price_margin_error()
        self.value = round(cost / (1 - margin),2) #Per project's instructions, this formula must be used to compute price
        self._cost = round(cost,2)
        self._margin = margin
        self.validate()

    @property
    def earning(self) -> float:
        return (self.price - self.cost)
    @property
    def price(self) -> float:
        return self.value
    @property
    def margin(self) -> float:
        return self._margin
    @property
    def cost(self) -> float:
        return self._cost

    def validate(self) -> None:
        if self.price < 0:
            raise invalid_product_price_error()
        if self.cost <= 0:
            raise invalid_product_cost_error()
        if (self.margin >= 1) or (self.margin < 0):
            raise invalid_product_price_margin_error()

    def __eq__(self, other: "ProductPricing") -> bool:
        return self.price == other.price

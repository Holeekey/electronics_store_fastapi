from typing import TypeVar
from common.domain.aggregate.aggregate import Aggregate
from product.domain.events.product_created import ProductCreated
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_price import ProductPrice
from .value_objects.product_name import ProductName

T = TypeVar("T", bound=ProductId)


class Product(Aggregate[T]):
    def __init__(self, id: ProductId, name: ProductName, price: ProductPrice) -> None:
        super().__init__(id)
        self._name = name
        self._price = price
        self.publish(ProductCreated(id, name, price))

    @property
    def name(self) -> ProductName:
        return self._name

    @property
    def price(self) -> ProductPrice:
        return self._price

    def validate_state(self) -> None:
        self._id.validate()
        self._name.validate()
        self._price.validate()

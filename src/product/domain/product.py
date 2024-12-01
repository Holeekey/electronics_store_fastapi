from typing import TypeVar
from common.domain.aggregate.aggregate import Aggregate
from product.domain.events.product_created import ProductCreated
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_price import ProductPrice
from .value_objects.product_name import ProductName
from .value_objects.product_status import ProductStatus

T = TypeVar("T", bound=ProductId)


class Product(Aggregate[T]):
    def __init__(self, id: ProductId, name: ProductName, price: ProductPrice, status:ProductStatus) -> None:
        super().__init__(id)
        self._name = name
        self._price = price
        self._status = status
        self.publish(ProductCreated(id, name, price))

    @property
    def name(self) -> ProductName:
        return self._name

    @property
    def price(self) -> ProductPrice:
        return self._price
    
    @property
    def status(self) -> ProductStatus:
        return self._status

    def validate_state(self) -> None:
        self._id.validate()
        self._name.validate()
        self._price.validate()
        self._status.validate()

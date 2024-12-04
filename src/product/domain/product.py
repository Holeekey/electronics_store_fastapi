from typing import TypeVar
from common.domain.aggregate.aggregate import Aggregate
from product.domain.events.product_created import ProductCreated
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_code import ProductCode
from product.domain.value_objects.product_description import ProductDescription
from product.domain.value_objects.product_pricing import ProductPricing
from .value_objects.product_name import ProductName
from .value_objects.product_status import ProductStatus

T = TypeVar("T", bound=ProductId)


class Product(Aggregate[T]):
    def __init__(self, id: ProductId, code: ProductCode, name: ProductName, description: ProductDescription, pricing: ProductPricing, status:ProductStatus) -> None:
        super().__init__(id)
        self._code = code
        self._name = name
        self._description = description
        self._pricing = pricing
        self._status = status
        self.publish(ProductCreated(id, name, pricing))

    @property
    def name(self) -> ProductName:
        return self._name

    @property
    def code(self) -> ProductCode:
        return self._code
    
    @property
    def description(self) -> ProductDescription:
        return self._description

    @property
    def pricing(self) -> ProductPricing:
        return self._pricing
    
    @property
    def status(self) -> ProductStatus:
        return self._status

    def validate_state(self) -> None:
        self._id.validate()
        self._code.validate()
        self._name.validate()
        self._description.validate()
        self._pricing.validate()
        self._status.validate()

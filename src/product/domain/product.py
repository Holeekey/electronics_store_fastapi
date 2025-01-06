from typing import TypeVar
from src.common.domain.aggregate.aggregate import Aggregate

from src.product.domain.events.product_created import ProductCreated
from src.product.domain.events.product_code_changed import ProductCodeChanged
from src.product.domain.events.product_name_changed import ProductNameChanged
from src.product.domain.events.product_description_changed import ProductDescriptionChanged
from src.product.domain.events.product_pricing_changed import ProductPricingChanged
from src.product.domain.events.product_deleted import ProductDeleted

from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_code import ProductCode
from src.product.domain.value_objects.product_description import ProductDescription
from src.product.domain.value_objects.product_pricing import ProductPricing
from src.product.domain.value_objects.product_name import ProductName
from src.product.domain.value_objects.product_status import ProductStatus, ProductStatusOptions

from src.product.domain.errors.product_already_deleted import product_already_deleted_error

T = TypeVar("T", bound=ProductId)


class Product(Aggregate[T]):
    def __init__(self, id: ProductId, code: ProductCode, name: ProductName, description: ProductDescription, pricing: ProductPricing, status:ProductStatus) -> None:
        super().__init__(id)
        self._code = code
        self._name = name
        self._description = description
        self._pricing = pricing
        self._status = status
        self.publish(ProductCreated(id, code, name, description, pricing))

    @property
    def name(self) -> ProductName:
        return self._name
    @name.setter
    def name(self, value:ProductName) -> None:
        self._name = value
        self.validate_state()
        self.publish(ProductNameChanged(self.id, self.name))

    @property
    def code(self) -> ProductCode:
        return self._code
    @code.setter
    def code(self, value:ProductCode) -> None:
        self._code = value
        self.validate_state()
        self.publish(ProductCodeChanged(self.id, self.code))
    
    @property
    def description(self) -> ProductDescription:
        return self._description
    @description.setter
    def description(self, value:ProductDescription) -> None:
        self._description = value
        self.validate_state()
        self.publish(ProductDescriptionChanged(self.id, self.description))

    @property
    def pricing(self) -> ProductPricing:
        return self._pricing
    @pricing.setter
    def pricing(self, value:ProductPricing) -> None:
        self._pricing = value
        self.validate_state()
        self.publish(ProductPricingChanged(self.id, self.pricing))
    
    @property
    def status(self) -> ProductStatus:
        return self._status

    def delete(self) -> None:
        if (self._status != ProductStatus(ProductStatusOptions.INACTIVE)):
            self._status = ProductStatus(ProductStatusOptions.INACTIVE)
            self.validate_state()
            self.publish(ProductDeleted(self.id))
        else:
            raise product_already_deleted_error()

    def validate_state(self) -> None:
        self._id.validate()
        self._code.validate()
        self._name.validate()
        self._description.validate()
        self._pricing.validate()
        self._status.validate()

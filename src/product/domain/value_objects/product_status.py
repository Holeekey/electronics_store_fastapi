from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_product_status import invalid_product_status_error
from enum import Enum

class ProductStatusOptions(Enum):
    ACTIVE = 1
    INACTIVE = 0

class ProductStatus(ValueObject):
    def __init__(self, status: ProductStatusOptions) -> None:
        self.value = status
        self.validate()

    @property
    def status(self) -> ProductStatusOptions:
        return self.value

    def validate(self) -> None:
        is_valid = False
        for value in ProductStatusOptions:
            if (self.status == value):
                is_valid = True
                break
        if (not is_valid):
            raise invalid_product_status_error()

    def __eq__(self, other: "ProductStatus") -> bool:
        return self.status == other.status
from src.common.domain.value_object.value_object import ValueObject
from src.order.domain.errors.invalid_order_status import invalid_order_status_error
from enum import Enum

class OrderStatusOptions(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderStatus(ValueObject):
    def __init__(self, status: OrderStatusOptions) -> None:
        self.value = status
        self.validate()

    @property
    def status(self) -> OrderStatusOptions:
        return self.value

    def is_cancelable(self) -> bool:
        return self.value.name != OrderStatusOptions.COMPLETED.name
    
    def is_completable(self) -> bool:
        return self.value.name != OrderStatusOptions.CANCELLED.name 

    def validate(self) -> None:
        is_valid = False
        for value in OrderStatusOptions:
            if (self.status == value):
                is_valid = True
                break
        if (not is_valid):
            raise invalid_order_status_error()

    def __eq__(self, other: "OrderStatus") -> bool:
        return self.status.name == other.status.name
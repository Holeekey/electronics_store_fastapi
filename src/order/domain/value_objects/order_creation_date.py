from datetime import datetime
from src.common.domain.value_object.value_object import ValueObject
from src.order.domain.errors.invalid_order_creation_date import invalid_order_creation_date_error


class OrderCreationDate(ValueObject):
    def __init__(self, date: datetime) -> None:
        self.value = date
        self.validate()

    @property
    def date(self) -> datetime:
        return self.value

    def validate(self) -> None:
        if not isinstance(self.value, datetime):
            raise invalid_order_creation_date_error()

    def __eq__(self, other: "OrderCreationDate") -> bool:
        return self.value == other.date
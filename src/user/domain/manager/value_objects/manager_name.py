from common.domain.utils.is_none import is_none
from common.domain.value_object.value_object import ValueObject
from user.domain.manager.errors import (
    invalid_manager_first_name,
    invalid_manager_last_name,
)


class ManagerName(ValueObject):
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.validate()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def validate(self) -> None:
        if is_none(self.first_name) or len(self.first_name) < 1:
            raise invalid_manager_first_name()

        if is_none(self.last_name) or len(self.last_name) < 1:
            raise invalid_manager_last_name()

    def __eq__(self, other: "ManagerName") -> bool:
        return self.first_name == other.first_name and self.last_name == other.last_name

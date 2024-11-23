from common.domain.utils.is_none import is_none
from common.domain.value_object.value_object import ValueObject
from user.domain.client.errors import (
    invalid_client_first_name,
    invalid_client_last_name,
)


class ClientName(ValueObject):
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.validate()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def validate(self) -> None:
        if is_none(self.first_name) | len(self.first_name) < 1:
            raise invalid_client_first_name()

        if is_none(self.last_name) | len(self.last_name) < 1:
            raise invalid_client_last_name()

    def __eq__(self, other: "ClientName") -> bool:
        return self.first_name == other.first_name and self.last_name == other.last_name

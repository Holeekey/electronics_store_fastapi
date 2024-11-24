from uuid import UUID
from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_client_id import invalid_client_id_error


class ClientId(ValueObject):
    def __init__(self, id: str) -> None:
        self.value = id
        self.validate()

    @property
    def id(self) -> str:
        return self.value

    def validate(self) -> None:
        try:
            UUID(self.id)
        except:
            raise invalid_client_id_error()

    def __eq__(self, other: "ClientId") -> bool:
        return self.value == other.id

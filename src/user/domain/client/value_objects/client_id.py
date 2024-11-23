from uuid import UUID
from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_client_id import invalid_client_id_error


class ClientId(ValueObject):
    def __init__(self, id: UUID) -> None:
        self.value = id
        self.validate()

    @property
    def id(self) -> UUID:
        return self.value

    def validate(self) -> None:
        if not isinstance(self.id, UUID):
            raise invalid_client_id_error()

    def __eq__(self, other: "ClientId") -> bool:
        return self.value == other.id

from uuid import UUID
from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_manager_id import invalid_manager_id_error


class ManagerId(ValueObject):
    def __init__(self, id: UUID) -> None:
        self.value = id
        self.validate()

    @property
    def id(self) -> UUID:
        return self.value

    def validate(self) -> None:
        if not isinstance(self.id, UUID):
            raise invalid_manager_id_error()

    def __eq__(self, other: "ManagerId") -> bool:
        return self.value == other.id

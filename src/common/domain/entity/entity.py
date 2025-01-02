from typing import Generic, TypeVar, Any
from src.common.domain.value_object.value_object import ValueObject

T = TypeVar("T", bound=ValueObject[Any])


class Entity(Generic[T]):
    def __init__(self, id: T):
        self._id = id

    @property
    def id(self) -> T:
        return self._id

    def __eq__(self, other: "Entity[T]") -> bool:
        return self._id.equals(other.id)

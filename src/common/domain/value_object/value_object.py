from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")


class ValueObject(ABC, Generic[T]):
    @abstractmethod
    def __eq__(self, other: "ValueObject[T]") -> bool:
        pass

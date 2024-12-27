from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod
from ..entity.entity import Entity
from ..value_object.value_object import ValueObject
from ..events.domain_event import DomainEvent

T = TypeVar("T", bound=ValueObject[Any])


class Aggregate(ABC, Generic[T], Entity[T]):
    def __init__(self, id: T) -> None:
        self._events: list[DomainEvent] = []
        super().__init__(id)

    @property
    def events(self) -> list[DomainEvent]:
        return self._events

    @abstractmethod
    def validate_state(self) -> None:
        pass

    def pull_events(self) -> list[DomainEvent]:
        events = self._events
        self._events = []
        return events
    
    def clear_events(self) -> None:
        self._events.clear()

    def publish(self, event: DomainEvent) -> None:
        self.validate_state()
        self._events.append(event)

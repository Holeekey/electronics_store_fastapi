from abc import ABCMeta, abstractmethod
from typing import Callable

from src.common.domain.events.domain_event import DomainEvent


class ISuscription(metaclass=ABCMeta):

    @abstractmethod
    async def unsubscribe(self) -> None:
        pass


class IEventHandler(metaclass=ABCMeta):

    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None:
        pass

    @abstractmethod
    async def subscribe(
        self, name: str, handler: Callable[[DomainEvent], None]
    ) -> ISuscription:
        pass


class IEventPublisher(metaclass=ABCMeta):

    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None:
        pass


class IEventListener(metaclass=ABCMeta):

    @abstractmethod
    async def subscribe(
        self, name: str, handler: Callable[[DomainEvent], None]
    ) -> ISuscription:
        pass

from common.application.event_handler.event_handler import IEventPublisher
from common.domain.events.domain_event import DomainEvent

from diator.events import DomainEvent as DiatorDomainEvent

from common.domain.utils.is_none import is_none
from common.infrastructure.events.diator.diator_event_adapter import DiatorEventAdapter


class DiatorEventMapper:
    def __init__(self, event: type, adapter: DiatorEventAdapter):
        self.event = event
        self.adapter = adapter


class DiatorEventPublisher(IEventPublisher):

    def __init__(self, event_mappers: list[DiatorEventMapper]):
        self._event_bus: list[DiatorDomainEvent] = []
        self._event_mappers = event_mappers

    def get_adapter(self, event: DomainEvent) -> DiatorEventAdapter:

        adapter = None

        for mapper in self._event_mappers:
            if mapper.event.__name__ == event.__class__.__name__:
                adapter = mapper.adapter
                break

        if is_none(adapter):
            raise Exception(f"Adapter not found for event {event.__class__.__name__}")

        return adapter

    def pull_events(self):
        events = self._event_bus
        self._event_bus = []
        return events

    async def publish(self, events: list[DomainEvent]):
        for event in events:
            self._event_bus.append(self.get_adapter(event)(event))

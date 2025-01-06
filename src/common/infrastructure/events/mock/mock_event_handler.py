from src.common.application.events.event_handlers import IEventHandler, IEventListener, IEventPublisher
from src.common.domain.events.domain_event import DomainEvent

class MockEventPublisher(IEventPublisher):
  def __init__(self):
    self.events = []

  async def publish(self, events: list[DomainEvent]):
    for event in events:
      self.events.append(event)

  async def clear(self):
    self.events = []
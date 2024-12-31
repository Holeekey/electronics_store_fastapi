from src.common.application.events.event_handlers import IEventHandler, IEventListener, IEventPublisher
from src.common.domain.events.domain_event import DomainEvent

class MockEventPublisher(IEventPublisher):
  def __init__(self):
    pass

  async def publish(self, events: list[DomainEvent]):
    for event in events:
      print(f"Event: {event.name} was published")
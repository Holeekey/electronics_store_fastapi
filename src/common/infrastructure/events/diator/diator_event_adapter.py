from typing import Callable, TypedDict

from diator.events import DomainEvent as DiatorDomainEvent

from common.domain.events.domain_event import DomainEvent

class DiatorEventAdapterParams(TypedDict):
    event: DomainEvent

DiatorEventAdapter = Callable[[DiatorEventAdapterParams], DiatorDomainEvent]

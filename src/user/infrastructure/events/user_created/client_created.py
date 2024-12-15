

import dataclasses
from common.domain.events.domain_event import DomainEvent
from user.domain.client.events.client_created import ClientCreated

@dataclasses.dataclass(frozen=True, kw_only=True)
class ClientCreatedDiator(DomainEvent):
    client_id: str = dataclasses.field()
    client_first_name: str = dataclasses.field()
    client_last_name: str = dataclasses.field()
    client_email: str = dataclasses.field()
    event_name: str = dataclasses.field()
    timestamp: str = dataclasses.field()
    
def client_created_diator_adapter(event: ClientCreated) -> ClientCreatedDiator:
    return ClientCreatedDiator(
        client_id=event.client_id.id,
        client_first_name=event.client_name.first_name,
        client_last_name=event.client_name.last_name,
        client_email=event.client_email.value,
        event_name=event.name,
        timestamp=event.event_time
    )
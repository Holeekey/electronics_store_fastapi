
import dataclasses
from diator.events.event import DomainEvent
from user.domain.manager.events.manager_created import ManagerCreated

@dataclasses.dataclass(frozen=True, kw_only=True)
class ManagerCreatedDiator(DomainEvent):
    manager_id: str = dataclasses.field()
    manager_first_name: str = dataclasses.field()
    manager_last_name: str = dataclasses.field()
    manager_email: str = dataclasses.field()
    event_name: str = dataclasses.field()
    timestamp: str = dataclasses.field()
    
def manager_created_diator_adapter(event: ManagerCreated) -> ManagerCreatedDiator:
    return ManagerCreatedDiator(
        manager_id=event.manager_id.id,
        manager_first_name=event.manager_name.first_name,
        manager_last_name=event.manager_name.last_name,
        manager_email=event.manager_email.value,
        event_name=event.name,
        timestamp=event.event_time
    )
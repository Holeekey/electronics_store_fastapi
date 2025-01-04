from src.common.domain.events.domain_event import DomainEvent
from src.user.domain.manager.value_objects.manager_id import ManagerId

MANAGER_ACTIVATED = "manager_activated"

class ManagerActivated(DomainEvent):
    def __init__(self, manager_id: ManagerId):
        super().__init__(MANAGER_ACTIVATED)
        self.manager_id = manager_id

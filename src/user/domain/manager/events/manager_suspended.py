from common.domain.events.domain_event import DomainEvent
from user.domain.manager.value_objects.manager_id import ManagerId

MANAGER_SUSPENDED = "manager_suspended"

class ManagerSuspended(DomainEvent):
    def __init__(self, manager_id: ManagerId):
        super().__init__(MANAGER_SUSPENDED)
        self.manager_id = manager_id

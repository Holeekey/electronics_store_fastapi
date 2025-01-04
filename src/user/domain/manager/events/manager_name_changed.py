from src.common.domain.events.domain_event import DomainEvent

from src.user.domain.manager.value_objects.manager_id import ManagerId
from src.user.domain.manager.value_objects.manager_name import ManagerName

MANAGER_NAME_CHANGED = "manager_name_changed"


class ManagerNameChanged(DomainEvent):
    def __init__(self, manager_id: ManagerId, name: ManagerName):
        super().__init__(MANAGER_NAME_CHANGED)
        self.manager_id = manager_id
        self.manager_name = name

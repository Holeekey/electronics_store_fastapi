from src.common.domain.events.domain_event import DomainEvent

from src.user.domain.manager.value_objects.manager_email import ManagerEmail
from src.user.domain.manager.value_objects.manager_id import ManagerId
from src.user.domain.manager.value_objects.manager_name import ManagerName

MANAGER_CREATED = "manager_created"

class ManagerCreated(DomainEvent):
    def __init__(self, manager_id: ManagerId, name: ManagerName, email: ManagerEmail):
        super().__init__(MANAGER_CREATED)
        self.manager_id = manager_id
        self.manager_name = name
        self.manager_email = email

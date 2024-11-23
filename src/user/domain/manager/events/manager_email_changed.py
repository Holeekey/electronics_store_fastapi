from common.domain.events.domain_event import DomainEvent

from user.domain.manager.value_objects.manager_email import ManagerEmail
from user.domain.manager.value_objects.manager_id import ManagerId

MANAGER_EMAIL_CHANGED = "manager_email_changed"


class ManagerEmailChanged(DomainEvent):
    def __init__(self, manager_id: ManagerId, email: ManagerEmail):
        super().__init__(MANAGER_EMAIL_CHANGED)
        self.manager_id = manager_id
        self.manager_email = email

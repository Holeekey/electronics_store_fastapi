from typing import TypeVar
from src.common.domain.aggregate.aggregate import Aggregate
from src.user.domain.manager.events.manager_created import ManagerCreated
from src.user.domain.manager.events.manager_email_changed import ManagerEmailChanged
from src.user.domain.manager.events.manager_name_changed import ManagerNameChanged
from src.user.domain.manager.events.manager_activated import ManagerActivated
from src.user.domain.manager.value_objects.manager_email import ManagerEmail
from src.user.domain.manager.value_objects.manager_id import ManagerId
from src.user.domain.manager.value_objects.manager_name import ManagerName
from src.user.domain.manager.events.manager_suspended import ManagerSuspended

T = TypeVar("T", bound=ManagerId)


class Manager(Aggregate[T]):
    def __init__(self, id: ManagerId, name: ManagerName, email: ManagerEmail) -> None:
        super().__init__(id)
        self._name = name
        self._email = email
        self.publish(ManagerCreated(id, name, email))

    @property
    def name(self) -> ManagerName:
        return self._name

    @name.setter
    def name(self, name: ManagerName) -> None:
        self._name = name
        self.publish(ManagerNameChanged(self.id, name))

    @property
    def email(self) -> ManagerEmail:
        return self._email

    @email.setter
    def email(self, email: ManagerEmail) -> None:
        self._email = email
        self.publish(ManagerEmailChanged(self.id, email))

    def __eq__(self, other: "Manager") -> bool:
        return self.id == other.id

    def suspend(self):
        self.publish(ManagerSuspended(self.id))
        
    def activate(self):
        self.publish(ManagerActivated(self.id))

    def validate_state(self) -> None:
        self._id.validate()
        self._name.validate()
        self._email.validate()

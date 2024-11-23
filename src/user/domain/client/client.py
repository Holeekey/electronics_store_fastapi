from typing import TypeVar
from common.domain.aggregate.aggregate import Aggregate
from user.domain.client.events.client_created import ClientCreated
from user.domain.client.events.client_email_changed import ClientEmailChanged
from user.domain.client.events.client_name_changed import ClientNameChanged
from user.domain.client.value_objects.client_email import ClientEmail
from user.domain.client.value_objects.client_id import ClientId
from user.domain.client.value_objects.client_name import ClientName

T = TypeVar("T", bound=ClientId)


class Client(Aggregate[T]):
    def __init__(self, id: ClientId, name: ClientName, email: ClientEmail) -> None:
        super().__init__(id)
        self._name = name
        self._email = email
        self.publish(ClientCreated(id, name, email))

    @property
    def name(self) -> ClientName:
        return self._name

    @name.setter
    def name(self, name: ClientName) -> None:
        self._name = name
        self.publish(ClientNameChanged(self.id, name))

    @property
    def email(self) -> ClientEmail:
        return self._email

    @email.setter
    def email(self, email: ClientEmail) -> None:
        self._email = email
        self.publish(ClientEmailChanged(self.id, email))

    def __eq__(self, other: "Client") -> bool:
        return self.id == other.id

    def validate_state(self) -> None:
        self._id.validate()
        self._name.validate()
        self._email.validate()

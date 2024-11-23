from common.domain.events.domain_event import DomainEvent

from user.domain.client.value_objects.client_email import ClientEmail
from user.domain.client.value_objects.client_id import ClientId
from user.domain.client.value_objects.client_name import ClientName

CLIENT_CREATED = "client_created"


class ClientCreated(DomainEvent):
    def __init__(self, client_id: ClientId, name: ClientName, email: ClientEmail):
        super().__init__(CLIENT_CREATED)
        self.client_id = client_id
        self.client_name = name
        self.client_email = email

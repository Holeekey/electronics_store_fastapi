from common.domain.events.domain_event import DomainEvent

from user.domain.client.value_objects.client_email import ClientEmail
from user.domain.client.value_objects.client_id import ClientId

CLIENT_EMAIL_CHANGED = "client_email_changed"


class ClientEmailChanged(DomainEvent):
    def __init__(self, client_id: ClientId, email: ClientEmail):
        super().__init__(CLIENT_EMAIL_CHANGED)
        self.client_id = client_id
        self.client_email = email

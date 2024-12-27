from common.domain.events.domain_event import DomainEvent

from user.domain.client.value_objects.client_id import ClientId
from user.domain.client.value_objects.client_name import ClientName

CLIENT_ACTIVATED = "client_activated"

class ClientActivated(DomainEvent):
    def __init__(self, client_id: ClientId):
        super().__init__(CLIENT_ACTIVATED)
        self.client_id = client_id

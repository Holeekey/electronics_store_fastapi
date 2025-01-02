from common.domain.events.domain_event import DomainEvent

from user.domain.client.value_objects.client_id import ClientId
from user.domain.client.value_objects.client_name import ClientName

CLIENT_SUSPENDED = "client_suspended"

class ClientSuspended(DomainEvent):
    def __init__(self, client_id: ClientId):
        super().__init__(CLIENT_SUSPENDED)
        self.client_id = client_id

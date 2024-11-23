from common.domain.events.domain_event import DomainEvent

from user.domain.client.value_objects.client_id import ClientId
from user.domain.client.value_objects.client_name import ClientName

CLIENT_NAME_CHANGED = "client_name_changed"


class ClientNameChanged(DomainEvent):
    def __init__(self, client_id: ClientId, name: ClientName):
        super().__init__(CLIENT_NAME_CHANGED)
        self.client_id = client_id
        self.client_name = name

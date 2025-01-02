from uuid import UUID
from src.user.domain.client.client import Client
from src.user.domain.client.value_objects.client_id import ClientId
from src.user.domain.client.value_objects.client_name import ClientName
from src.user.domain.client.value_objects.client_email import ClientEmail


def client_factory(id: str, first_name: str, last_name: str, email: str):

    client_id = ClientId(UUID(id))
    client_name = ClientName(first_name, last_name)
    client_email = ClientEmail(email)

    return Client(client_id, client_name, client_email)

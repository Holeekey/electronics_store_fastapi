from abc import ABCMeta, abstractmethod
from typing import List, Optional

from user.domain.client.client import Client
from user.domain.client.value_objects.client_id import ClientId


class IClientRepository(metaclass=ABCMeta):
    @abstractmethod
    async def find_one(self, id: ClientId) -> Optional[Client]:
        pass

    @abstractmethod
    async def find_all(self) -> Optional[List[Client]]:
        pass

from abc import ABCMeta, abstractmethod
from typing import List, Optional

from user.domain.manager.manager import Manager
from user.domain.manager.value_objects.manager_id import ManagerId


class IManagerRepository(metaclass=ABCMeta):
    @abstractmethod
    async def find_one(self, id: ManagerId) -> Optional[Manager]:
        pass

    @abstractmethod
    async def find_all(self) -> Optional[List[Manager]]:
        pass

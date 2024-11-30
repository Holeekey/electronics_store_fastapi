from abc import ABCMeta, abstractmethod
from typing import List, Optional

from common.domain.result.result import Result
from user.application.models.user import User, UserRole


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    async def find_one(self, id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_login_credential(self, login_credential: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_role(self, role: UserRole) -> Optional[List[User]]:
        pass

    @abstractmethod
    async def find_all(self) -> Optional[List[User]]:
        pass

    @abstractmethod
    async def save(self, user: User) -> Result[User]:
        pass

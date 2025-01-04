from typing import List
from src.user.application.repositories.manager_repository import IManagerRepository
from src.user.domain.manager.value_objects.manager_id import ManagerId
from src.user.application.models.user import User
from src.user.domain.manager.factories import manager_factory


class ManagerRepositoryMock(IManagerRepository):

    users: List[User]

    def __init__(self):
        self.users = []

    async def find_one(self, id: ManagerId):
        for user in self.users:
            print(f"{user} | {user.id} | {id} | {id.value}")
            if user.id == id.value:
                return manager_factory(
                    id= user.id,
                    first_name= user.first_name,
                    last_name= user.last_name,
                    email= user.email
                  )
        return None

    async def find_all(self):
        return [
            manager_factory(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            for user in self.users
          ] 

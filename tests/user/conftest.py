import pytest

from src.user.infrastructure.repositories.mock.user_repository import UserRepositoryMock
from src.user.infrastructure.routes.types.create.create_user_dto import CreateUserDto, UserRole
from src.user.infrastructure.repositories.mock.manager_repository import ManagerRepositoryMock

def user_payload(username= "JohnDoe", password= "password", first_name= "John", last_name= "Doe", email= "JohnDoe@email.com", role= UserRole.CLIENT):
  return CreateUserDto(username= username,
                       password= password,
                       first_name= first_name,
                       last_name= last_name,
                       email= email,
                       role= role)
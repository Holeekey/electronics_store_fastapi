import pytest


from src.config import TEMP_DATABASE_URL

from src.user.infrastructure.repositories.mock.user_repository import UserRepositoryMock
from src.common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from src.common.infrastructure.cryptography.single_caesar.single_caesar_cryptography_provider import SingleCaesarProvider
from src.common.infrastructure.events.mock.mock_event_handler import MockEventPublisher
from src.user.infrastructure.routes.types.create.create_user_dto import CreateUserDto, UserRole

#Fixtures
@pytest.fixture()
def mock_user_repository():
  return UserRepositoryMock()

@pytest.fixture()
def id_generator():
  return UUIDGenerator()

@pytest.fixture()
def caesar_cypher_provider():
  return SingleCaesarProvider()

@pytest.fixture()
def mock_publisher():
  return MockEventPublisher()

@pytest.fixture()
def client_payload():
  return CreateUserDto(
    username= "John Doe",
    password= "password",
    first_name= "John",
    last_name= "Doe",
    email= "JohnDoe@email.com",
    role= UserRole.CLIENT
  )

@pytest.fixture()
def manager_payload():
  return CreateUserDto(
    username= "John Doe",
    password= "password",
    first_name= "John",
    last_name= "Doe",
    email= "JohnDoe@email.com",
    role= UserRole.MANAGER
  )
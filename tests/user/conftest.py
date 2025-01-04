import pytest

from src.user.infrastructure.repositories.mock.user_repository import UserRepositoryMock
from src.user.infrastructure.routes.types.create.create_user_dto import CreateUserDto, UserRole
from src.user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.manager_repository import ManagerRepositorySqlAlchemy
from src.user.infrastructure.repositories.mock.manager_repository import ManagerRepositoryMock
from src.user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy

# id_generator = UUIDGenerator()
# mock_user_repository = UserRepositoryMock()
# caesar_cypher_provider = SingleCaesarProvider()
# mock_publisher = MockEventPublisher()

def user_payload(username= "JohnDoe", password= "password", first_name= "John", last_name= "Doe", email= "JohnDoe@email.com", role= UserRole.CLIENT):
  return CreateUserDto(username= username,
                       password= password,
                       first_name= first_name,
                       last_name= last_name,
                       email= email,
                       role= role)

#Fixtures
@pytest.fixture()
def mock_user_repository():
  return UserRepositoryMock()

@pytest.fixture()
def mock_manager_repository():
  return ManagerRepositoryMock()

@pytest.fixture()
def temp_user_repository(temp_db_session):
  return UserRepositorySqlAlchemy(temp_db_session)

@pytest.fixture()
def temp_manager_repository(temp_db_session):
  return ManagerRepositorySqlAlchemy(temp_db_session)

@pytest.fixture()
def temp_client_repository(temp_db_session):
  return ClientRepositorySqlAlchemy(temp_db_session)
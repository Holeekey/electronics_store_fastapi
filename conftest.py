import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import ProductRepositorySqlAlchemy
from src.common.infrastructure.cryptography.single_caesar.single_caesar_cryptography_provider import SingleCaesarProvider
from src.common.infrastructure.events.mock.mock_event_handler import MockEventPublisher
from src.common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from src.common.infrastructure.token.jwt.jwt_provider import get_jwt_provider
from src.user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.manager_repository import ManagerRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy

from src.config import TEMP_DATABASE_URL

engine = create_engine(
  url= TEMP_DATABASE_URL,
  poolclass= StaticPool
)

TempSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def temp_db_session():
  connection = engine.connect()
  transaction = connection.begin()
  session = TempSession(bind=connection)
  yield session
  session.close()
  transaction.rollback()
  connection.close()

@pytest.fixture()
def temp_product_repository(temp_db_session):
  return ProductRepositorySqlAlchemy(temp_db_session)

@pytest.fixture()
def temp_user_repository(temp_db_session):
  return UserRepositorySqlAlchemy(temp_db_session)

@pytest.fixture()
def temp_manager_repository(temp_db_session):
  return ManagerRepositorySqlAlchemy(temp_db_session)

@pytest.fixture()
def temp_client_repository(temp_db_session):
  return ClientRepositorySqlAlchemy(temp_db_session)

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
def token_provider():
  return get_jwt_provider()
import pytest

from src.shopping_cart.infrastructure.repositories.postgres.sqlalchemy.shopping_cart_repository import ShoppingCartRepositorySqlAlchemy


@pytest.fixture()
def temp_shopping_cart_repository(temp_db_session):
  return ShoppingCartRepositorySqlAlchemy(temp_db_session)
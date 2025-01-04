import pytest

from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import ProductRepositorySqlAlchemy
from src.inventory.infrastructure.repositories.postgres.sqlalchemy.inventory_repository import InventoryRepositorySqlAlchemy

@pytest.fixture()
def temp_inventory_repository(temp_db_session):
  return InventoryRepositorySqlAlchemy(temp_db_session)
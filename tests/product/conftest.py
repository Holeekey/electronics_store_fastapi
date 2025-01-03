import pytest

from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import ProductRepositorySqlAlchemy


from src.product.application.commands.create.types.dto import CreateProductDto

def product_payload(code= "TEST-00", name= "TestProduct", description= "Test Description", cost= 1.0, margin= 0.5) -> CreateProductDto:
  return CreateProductDto(
    code= code,
    name= name,
    description= description,
    cost= cost,
    margin= margin
  )

@pytest.fixture()
def temp_product_repository(temp_db_session):
  return ProductRepositorySqlAlchemy(temp_db_session)
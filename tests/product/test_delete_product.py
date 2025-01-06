import pytest
import asyncio
import pytest_asyncio

from src.product.application.commands.delete.types.dto import DeleteProductDto
from src.product.application.commands.delete.delete_product_command import DeleteProductCommand
from src.product.application.commands.create.create_product_command import CreateProductCommand
from src.product.domain.value_objects.product_id import ProductId
from tests.product.conftest import product_payload

@pytest.mark.asyncio
async def test_delete_product_successfully(id_generator, temp_product_repository, mock_publisher):
  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository,
    publisher=mock_publisher
  )

  result = await command.execute(product_payload())

  assert result.is_success()

  created_product_id = result.unwrap().product_id

  command = DeleteProductCommand(product_repository= temp_product_repository, publisher=mock_publisher)

  result = await command.execute(DeleteProductDto(created_product_id))

  assert result.is_success()
  assert result._info.code == "PR-DEL"
  assert result._info.message == "Product has been deactivated successfully"

  deleted_product_id = result.unwrap().id
  assert deleted_product_id == created_product_id

  deleted_product = await temp_product_repository.find_one(ProductId(created_product_id))

  assert deleted_product == None

@pytest.mark.asyncio
async def test_delete_failure_user_not_found(id_generator, temp_product_repository, mock_publisher):
  command = DeleteProductCommand(product_repository= temp_product_repository, publisher=mock_publisher)

  result = await command.execute(DeleteProductDto(id_generator.generate()))

  assert result.is_error()
  assert result._error.code == "PR-E-NF"
  assert result._error.message == "Product not found"
import pytest
import asyncio
import pytest_asyncio

from src.product.application.commands.create.create_product_command import CreateProductCommand
from tests.product.conftest import product_payload


@pytest.mark.asyncio
async def test_create_product_successfully(id_generator, temp_product_repository):
  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())

  assert result.is_success()
  assert result._info.code == "PR-001"
  assert result._info.message == "Product created successfully"

  product_id = result.unwrap().product_id
  created_product = await temp_product_repository.find_one(product_id)

  assert created_product.code.value == "TEST-00"
  assert created_product.name.value == "TestProduct"
  assert created_product.description.value == "Test Description"


@pytest.mark.asyncio
async def test_create_product_failure_name_already_exists(id_generator, temp_product_repository):
  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())
  assert result.is_success()

  result = await command.execute(product_payload())
  
  assert result.is_error()
  assert result._error.code == "PR-E-001"
  assert result._error.message == "Product name already exists"
import pytest
import asyncio
import pytest_asyncio

from src.product.domain.value_objects.product_id import ProductId
from src.product.application.commands.create.create_product_command import CreateProductCommand
from src.inventory.application.commands.types.create_inventory_dto import CreateInventoryDto
from src.inventory.application.commands.create.create_inventory_command import CreateOrUpdateInventoryCommand
from tests.product.conftest import product_payload


@pytest.mark.asyncio
async def test_create_inventory_successfully(id_generator, temp_inventory_repository, temp_product_repository):
  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())

  assert result.is_success()
  product_id = result.unwrap().product_id.id

  command = CreateOrUpdateInventoryCommand(
    id_generator= id_generator,
    inventory_repository= temp_inventory_repository,
    product_repository= temp_product_repository
  )

  result = await command.execute(CreateInventoryDto(product_id, 1))

  assert result.is_success()
  assert result._info.code == "INV-001"
  assert result._info.message == "Inventory created successfully"

  response = result.unwrap()

  created_inventory = await temp_inventory_repository.find_by_product_id(ProductId(product_id))

  assert response.inventory_id == created_inventory.id
  assert created_inventory.product_id.id == product_id
  assert created_inventory.stock.value == 1

@pytest.mark.asyncio
async def test_update_inventory_successfully(id_generator, temp_inventory_repository, temp_product_repository):
  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())

  assert result.is_success()
  product_id = result.unwrap().product_id.id

  command = CreateOrUpdateInventoryCommand(
    id_generator= id_generator,
    inventory_repository= temp_inventory_repository,
    product_repository= temp_product_repository
  )

  result = await command.execute(CreateInventoryDto(product_id, 1))
  assert result.is_success()

  result = await command.execute(CreateInventoryDto(product_id, 2))

  assert result.is_success()
  assert result._info.code == "INV-003"
  assert result._info.message == "Inventory updated successfully"

  response = result.unwrap()

  created_inventory = await temp_inventory_repository.find_by_product_id(ProductId(product_id))

  assert response.inventory_id == created_inventory.id
  assert created_inventory.product_id.id == product_id
  assert created_inventory.stock.value == 2

@pytest.mark.asyncio
async def test_create_failure_product_not_found(id_generator, temp_inventory_repository, temp_product_repository):
  command = CreateOrUpdateInventoryCommand(
    id_generator= id_generator,
    inventory_repository= temp_inventory_repository,
    product_repository= temp_product_repository
  )
  product_id = id_generator.generate()
  result = await command.execute(CreateInventoryDto(product_id, 1))

  assert result.is_error()
  assert result._error.code == "INV-E-003"
  assert result._error.message == "Product does not exist"
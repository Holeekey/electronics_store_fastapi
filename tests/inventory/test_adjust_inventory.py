import pytest
import asyncio
import pytest_asyncio

from src.product.domain.value_objects.product_id import ProductId
from src.inventory.application.commands.types.adjust_inventory_dto import AdjustInventoryDto
from src.inventory.application.commands.adjust.adjust_inventory_command import AdjustInventoryCommand
from src.product.application.commands.create.create_product_command import CreateProductCommand
from tests.product.conftest import product_payload

@pytest.mark.asyncio
async def test_adjust_inventory_successfully(id_generator, temp_inventory_repository, temp_product_repository, mock_publisher):
  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository,
    publisher=mock_publisher
  )

  result = await command.execute(product_payload())

  assert result.is_success()
  product_id = result.unwrap().product_id

  command = AdjustInventoryCommand(
    id_generator= id_generator,
    inventory_repository= temp_inventory_repository,
    product_repository= temp_product_repository
  )

  result = await command.execute(AdjustInventoryDto(product_id= product_id, stock_change= 1))
  assert result.is_success()

  result = await command.execute(AdjustInventoryDto(product_id= product_id, stock_change= 1))


  assert result.is_success()
  assert result._info.code == "INV-003"
  assert result._info.message == "Inventory updated successfully"

  adjusted_product = await temp_inventory_repository.find_by_product_id(ProductId(product_id))
  assert adjusted_product.stock.value == 2


@pytest.mark.asyncio
async def test_adjust_failure_product_not_found(id_generator, temp_inventory_repository, temp_product_repository):
  command = AdjustInventoryCommand(
    id_generator= id_generator,
    inventory_repository= temp_inventory_repository,
    product_repository= temp_product_repository
  )
  product_id = id_generator.generate()
  result = await command.execute(AdjustInventoryDto(product_id, 1))

  assert result.is_error()
  assert result._error.code == "INV-E-003"
  assert result._error.message == "Product does not exist"
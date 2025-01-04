import pytest
import asyncio
import pytest_asyncio

from src.product.application.commands.update.types.dto import UpdateProductDto
from src.product.application.commands.update.update_product_command import UpdateProductCommand
from src.product.application.commands.create.create_product_command import CreateProductCommand
from tests.product.conftest import product_payload


@pytest.mark.asyncio
async def test_update_product_successfully(id_generator, temp_product_repository):
  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())

  assert result.is_success()

  created_product_id = result.unwrap().product_id

  command = UpdateProductCommand(product_repository= temp_product_repository)

  result = await command.execute(UpdateProductDto(
    id= created_product_id.id,
    code= "TEST-002",
    name= "NewName",
    description= "New Description",
    cost= 2.0,
    margin= 0.25
  ))

  assert result.is_success()
  assert result._info.code == "UPD-001"
  assert result._info.message == "Product updated successfully"

  response = result.unwrap()

  assert response.code == "TEST-002"
  assert response.name == "NewName"
  assert response.description == "New Description"
  

@pytest.mark.asyncio
async def test_update_failure_product_not_found(id_generator, temp_product_repository):
  command = UpdateProductCommand(product_repository= temp_product_repository)
  
  result = await command.execute(UpdateProductDto(
    id= id_generator.generate(),
    code= "TEST-002",
    name= "NewName",
    description= "New Description",
    cost= 2.0,
    margin= 0.25
  ))

  assert result.is_error
  assert result._error.code == "PR-E-NF"
  assert result._error.message == "Product not found"



  
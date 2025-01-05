from uuid import UUID
import pytest
import asyncio
import pytest_asyncio

from src.product.domain.value_objects.product_id import ProductId
from src.shopping_cart.application.services.remove_item.types.dto import RemoveItemFromShoppingCartDto
from src.shopping_cart.application.services.remove_item.remove_item_from_shopping_cart_service import RemoveItemFromShoppingCartService
from src.product.application.commands.create.create_product_command import CreateProductCommand
from src.shopping_cart.application.services.add_items.add_items_to_shopping_cart_service import AddItemsToShoppingCartService
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartDto, ItemDetail
from src.user.application.commands.create.create_user_command import CreateUserCommand
from tests.product.conftest import product_payload
from tests.user.conftest import user_payload
from src.user.domain.client.value_objects.client_id import ClientId

@pytest.mark.asyncio
async def test_remove_item_from_cart_successfully(id_generator, temp_user_repository, temp_client_repository,temp_product_repository, temp_shopping_cart_repository, mock_publisher, caesar_cypher_provider):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload())


  assert result.is_success()
  user_id = result.unwrap().user_id

  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())

  assert result.is_success()
  product_id = result.unwrap().product_id.value

  await mock_publisher.clear()

  command = AddItemsToShoppingCartService(
    id_generator= id_generator,
    client_repository= temp_client_repository,
    product_repository= temp_product_repository,
    shopping_cart_repository= temp_shopping_cart_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(AddItemsToShoppingCartDto(
    client_id= user_id,
    items= [ItemDetail(product_id, 1)]
  ))

  assert result.is_success()

  command = RemoveItemFromShoppingCartService(
    client_repository= temp_client_repository,
    shopping_cart_repository= temp_shopping_cart_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(RemoveItemFromShoppingCartDto(
    product_id= product_id,
    client_id= user_id
  ))

  assert result.is_success()
  assert result._info.code == "SC-002"
  assert result._info.message == "Item removed from shopping cart successfully"

  cart = await temp_shopping_cart_repository.find_by_client_id(ClientId(UUID(user_id)))

  assert cart.has_item(ProductId(product_id)) == False

@pytest.mark.asyncio
async def test_remove_failure_client_not_found(id_generator, temp_product_repository, mock_publisher, temp_client_repository, temp_shopping_cart_repository, temp_user_repository, caesar_cypher_provider):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload())


  assert result.is_success()
  user_id = result.unwrap().user_id

  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())

  assert result.is_success()
  product_id = result.unwrap().product_id.value

  await mock_publisher.clear()

  command = AddItemsToShoppingCartService(
    id_generator= id_generator,
    client_repository= temp_client_repository,
    product_repository= temp_product_repository,
    shopping_cart_repository= temp_shopping_cart_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(AddItemsToShoppingCartDto(
    client_id= user_id,
    items= [ItemDetail(product_id, 1)]
  ))

  assert result.is_success()

  command = RemoveItemFromShoppingCartService(
    client_repository= temp_client_repository,
    shopping_cart_repository= temp_shopping_cart_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(RemoveItemFromShoppingCartDto(
    product_id= product_id,
    client_id= id_generator.generate()
  ))

  assert result.is_error()
  assert result._error.code == "SC-E-001"
  assert result._error.message == "Client not found"

@pytest.mark.asyncio
async def test_remove_failure_product_not_in_cart(id_generator, temp_product_repository, mock_publisher, temp_client_repository, temp_shopping_cart_repository, temp_user_repository, caesar_cypher_provider):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload())


  assert result.is_success()
  user_id = result.unwrap().user_id

  command = CreateProductCommand(
    id_generator= id_generator,
    product_repository= temp_product_repository
  )

  result = await command.execute(product_payload())

  assert result.is_success()
  product_id = result.unwrap().product_id.value

  await mock_publisher.clear()

  command = AddItemsToShoppingCartService(
    id_generator= id_generator,
    client_repository= temp_client_repository,
    product_repository= temp_product_repository,
    shopping_cart_repository= temp_shopping_cart_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(AddItemsToShoppingCartDto(
    client_id= user_id,
    items= [ItemDetail(product_id, 1)]
  ))

  assert result.is_success()

  command = RemoveItemFromShoppingCartService(
    client_repository= temp_client_repository,
    shopping_cart_repository= temp_shopping_cart_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(RemoveItemFromShoppingCartDto(
    product_id= id_generator.generate(),
    client_id= user_id
  ))

  assert result.is_error()
  assert result._error.code == "SC-E-003"
  assert result._error.message == "Client's shopping cart does not include the product"
  
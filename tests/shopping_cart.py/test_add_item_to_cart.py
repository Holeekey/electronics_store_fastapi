from uuid import UUID
import pytest
import asyncio
import pytest_asyncio

from src.product.domain.value_objects.product_id import ProductId
from src.product.application.commands.create.create_product_command import CreateProductCommand
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartDto, ItemDetail
from src.shopping_cart.application.services.add_items.add_items_to_shopping_cart_service import AddItemsToShoppingCartService
from tests.product.conftest import product_payload
from tests.user.conftest import user_payload
from src.user.application.commands.create.create_user_command import CreateUserCommand
from src.user.domain.client.value_objects.client_id import ClientId

@pytest.mark.asyncio
async def test_add_item_to_cart_successfully(id_generator, temp_user_repository, temp_client_repository,temp_product_repository, temp_shopping_cart_repository, mock_publisher, caesar_cypher_provider):
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
  assert result._info.code == "SC-001"
  assert result._info.message == "Items added to shopping cart successfully"

  response = result.unwrap()

  assert response.message == "Succesful"

  cart = await temp_shopping_cart_repository.find_by_client_id(ClientId(UUID(user_id)))

  assert cart.has_item(ProductId(product_id))

  assert len(mock_publisher.events) == 1
  assert mock_publisher.events[0].name == "shopping_cart_items_added"


@pytest.mark.asyncio
async def test_add_item_failure_client_not_found(id_generator, temp_product_repository, temp_client_repository, temp_shopping_cart_repository, mock_publisher):
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
    client_id= id_generator.generate(),
    items= [ItemDetail(product_id, 1)]
  ))

  assert result.is_error()
  assert result._error.code == "SC-E-001"
  assert result._error.message == "Client not found"

@pytest.mark.asyncio
async def test_add_item_failure_product_not_found(id_generator, temp_product_repository, temp_client_repository, temp_shopping_cart_repository, temp_user_repository, caesar_cypher_provider, mock_publisher):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload())


  assert result.is_success()
  user_id = result.unwrap().user_id

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
    items= [ItemDetail(id_generator.generate(), 1)]
  ))

  assert result.is_error()
  assert result._error.code == "SC-E-002"
  assert result._error.message == "Product not found"
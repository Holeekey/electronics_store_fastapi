import pytest
import asyncio
import pytest_asyncio
from src.user.application.commands.create.create_user_command import CreateUserCommand
from tests.user.conftest import user_payload
from src.user.infrastructure.routes.types.create.create_user_dto import UserRole


@pytest.mark.asyncio
async def test_create_client_succesfully(id_generator, temp_user_repository, mock_publisher, caesar_cypher_provider):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload())


  assert result.is_success()
  assert result._info.code.value == "US-001"
  assert result._info.message == "User created successfully"
  
  response = result.unwrap()
  created_user = await temp_user_repository.find_one(response.user_id)
  assert created_user.username == "JohnDoe"
  assert caesar_cypher_provider.decrypt(created_user.password) == "password"
  assert created_user.first_name == "John"
  assert created_user.last_name == "Doe"
  assert created_user.email == "JohnDoe@email.com"
  assert created_user.role.value == UserRole.CLIENT.value

  assert len(mock_publisher.events) == 1
  assert mock_publisher.events[0].name == "client_created"

@pytest.mark.asyncio
async def test_create_manager_succesfully(id_generator, temp_user_repository, mock_publisher, caesar_cypher_provider):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload(role= UserRole.MANAGER))


  assert result.is_success()
  assert result._info.code.value == "US-001"
  assert result._info.message == "User created successfully"
  
  response = result.unwrap()
  created_user = await temp_user_repository.find_one(response.user_id)
  assert created_user.username == "JohnDoe"
  assert caesar_cypher_provider.decrypt(created_user.password) == "password"
  assert created_user.first_name == "John"
  assert created_user.last_name == "Doe"
  assert created_user.email == "JohnDoe@email.com"
  assert created_user.role.value == UserRole.MANAGER.value

  assert len(mock_publisher.events) == 1
  assert mock_publisher.events[0].name == "manager_created"

@pytest.mark.asyncio
async def test_failure_username_already_exists(id_generator, temp_user_repository, mock_publisher, caesar_cypher_provider):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload())

  result = await command.execute(user_payload())

  assert result.is_error()
  assert result._error.code == "US-E-001" 
  assert result._error.message == "Username already used"


@pytest.mark.asyncio
async def test_failure_email_already_exists(id_generator, temp_user_repository, mock_publisher, caesar_cypher_provider):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= temp_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(user_payload())

  result = await command.execute(user_payload(username= "DifferentUsername"))

  assert result.is_error()
  assert result._error.code == "US-E-002"
  assert result._error.message == "Email already used"



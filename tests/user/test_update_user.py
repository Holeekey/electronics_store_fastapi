import pytest
import asyncio
import pytest_asyncio

from src.user.application.commands.create.create_user_command import CreateUserCommand
from tests.user.conftest import user_payload
from src.user.application.commands.update.update_user_command import UpdateUserCommand
from src.user.application.commands.update.types.dto import UpdateUserDto
from src.user.application.models.user import UserRole, UserStatus


@pytest.mark.asyncio
async def test_update_user_successfully(id_generator, temp_user_repository, temp_manager_repository, temp_client_repository, caesar_cypher_provider, mock_publisher):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()
  user_id = result.unwrap().user_id

  command = UpdateUserCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    client_repository= temp_client_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )

  result = await command.execute(UpdateUserDto(
    id = user_id,
    username= "NewUsername",
    password= "NewPassword",
    email= "NewEmail@email.com",
    first_name= "NewFirstName",
    last_name= "NewLastName",
    status= UserStatus.SUSPENDED
  ))

  assert result.is_success()
  assert result._info.code.value == "US-006"
  assert result._info.message == "User updated successfully"

  response = result.unwrap()

  assert response.id == user_id
  assert response.username == "NewUsername"
  assert response.email == "NewEmail@email.com"
  assert response.first_name == "NewFirstName"
  assert response.last_name == "NewLastName"
  assert response.status.name == "SUSPENDED"

  updated_user = await temp_user_repository.find_one(user_id)

  assert updated_user.username == "NewUsername"
  assert caesar_cypher_provider.decrypt(updated_user.password) == "NewPassword"
  assert updated_user.email == "NewEmail@email.com"
  assert updated_user.first_name == "NewFirstName"
  assert updated_user.last_name == "NewLastName"
  assert updated_user.status.name == "SUSPENDED"

  assert len(mock_publisher.events) == 4
  assert mock_publisher.events[1].name == "client_email_changed"
  assert mock_publisher.events[2].name == "client_name_changed"
  assert mock_publisher.events[3].name == "client_suspended"


@pytest.mark.asyncio
async def test_update_user_failure_user_not_found(id_generator, temp_user_repository, temp_manager_repository, temp_client_repository, caesar_cypher_provider, mock_publisher):
  command = UpdateUserCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    client_repository= temp_client_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )

  result = await command.execute(UpdateUserDto(
    id = id_generator.generate(),
    username= "NewUsername"
  ))

  assert result.is_error()
  assert result._error.code == "US-E-NF"
  assert result._error.message == "User not found"


@pytest.mark.asyncio
async def test_update_user_failure_user_is_not_manager(id_generator, temp_user_repository, temp_manager_repository, temp_client_repository, caesar_cypher_provider, mock_publisher):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()
  user_id = result.unwrap().user_id
  
  command = UpdateUserCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    client_repository= temp_client_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )

  result = await command.execute(UpdateUserDto(
    id = user_id,
    role_to_update= UserRole.MANAGER
  ))

  assert result.is_error()
  assert result._error.code == "US-E-005"
  assert result._error.message == "User is not a manager"

@pytest.mark.asyncio
async def test_update_user_failure_user_is_not_client(id_generator, temp_user_repository, temp_manager_repository, temp_client_repository, caesar_cypher_provider, mock_publisher):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload(role= UserRole.MANAGER))
  
  assert result.is_success()
  user_id = result.unwrap().user_id
  
  command = UpdateUserCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    client_repository= temp_client_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )

  result = await command.execute(UpdateUserDto(
    id = user_id,
    role_to_update= UserRole.CLIENT
  ))

  assert result.is_error()
  assert result._error.code == "US-E-006"
  assert result._error.message == "User is not a client"

@pytest.mark.asyncio
async def test_update_user_failure_user_is_not_admin(id_generator, temp_user_repository, temp_manager_repository, temp_client_repository, caesar_cypher_provider, mock_publisher):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()
  user_id = result.unwrap().user_id
  
  command = UpdateUserCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    client_repository= temp_client_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )

  result = await command.execute(UpdateUserDto(
    id = user_id,
    role_to_update= UserRole.ADMIN
  ))

  assert result.is_error()
  assert result._error.code == "US-E-007"
  assert result._error.message == "User is not an admin"

@pytest.mark.asyncio
async def test_update_user_failure_email_already_used(id_generator, temp_user_repository, temp_manager_repository, temp_client_repository, caesar_cypher_provider, mock_publisher):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()
  user_id = result.unwrap().user_id
  
  result = await command.execute(user_payload(username="JohnDoe1", email="JohnDoe1@email.com"))
  
  command = UpdateUserCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    client_repository= temp_client_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )

  result = await command.execute(UpdateUserDto(
    id = user_id,
    email= "JohnDoe1@email.com"
  ))

  assert result.is_error()
  assert result._error.code == "US-E-002"
  assert result._error.message == "Email already used"

@pytest.mark.asyncio
async def test_update_user_failure_username_already_used(id_generator, temp_user_repository, temp_manager_repository, temp_client_repository, caesar_cypher_provider, mock_publisher):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()
  user_id = result.unwrap().user_id
  
  result = await command.execute(user_payload(username="JohnDoe1", email="JohnDoe1@email.com"))
  
  command = UpdateUserCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    client_repository= temp_client_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )

  result = await command.execute(UpdateUserDto(
    id = user_id,
    username= "JohnDoe1"
  ))

  assert result.is_error()
  assert result._error.code == "US-E-001"
  assert result._error.message == "Username already used"


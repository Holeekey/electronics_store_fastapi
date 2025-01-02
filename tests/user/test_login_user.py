import pytest
import asyncio
import pytest_asyncio

from src.user.application.commands.create.create_user_command import CreateUserCommand
from tests.user.conftest import user_payload
from src.user.infrastructure.routes.types.create.create_user_dto import UserRole
from src.user.application.commands.login.login_command import LoginCommand
from src.user.infrastructure.routes.types.login.login_dto import LoginDto
from src.user.application.commands.update.update_user_command import UpdateUserCommand
from src.user.infrastructure.routes.types.update.update_user_dto import UserStatus
from src.user.application.commands.update.types.dto import UpdateUserDto


@pytest.mark.asyncio
async def test_user_login_successfully_by_username(id_generator, temp_user_repository, mock_publisher, caesar_cypher_provider, token_provider):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()
  user_id = result.unwrap().user_id

  user = await temp_user_repository.find_one(user_id)

  command = LoginCommand(
    user_repository= temp_user_repository,
    token_provider= token_provider,
    cryptography_provider= caesar_cypher_provider
  )

  result = await command.execute(LoginDto(
    login_credential= user.username, 
    password= caesar_cypher_provider.decrypt(user.password))
  )

  assert result.is_success()
  assert result._info.code.value == "US-003"
  assert result._info.message == "User logged in successfully"

@pytest.mark.asyncio
async def test_user_login_succesfully_by_email(id_generator, temp_user_repository, mock_publisher, caesar_cypher_provider, token_provider):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()

  command = LoginCommand(
    user_repository= temp_user_repository,
    token_provider= token_provider,
    cryptography_provider= caesar_cypher_provider
  )

  result = await command.execute(LoginDto(
    login_credential= "JohnDoe@email.com", 
    password= "password")
  )

  assert result.is_success()
  assert result._info.code.value == "US-003"
  assert result._info.message == "User logged in successfully"

@pytest.mark.asyncio
async def test_user_login_failure_invalid_credentials(temp_user_repository, token_provider, caesar_cypher_provider):
  
  command = LoginCommand(
    user_repository= temp_user_repository,
    token_provider= token_provider,
    cryptography_provider= caesar_cypher_provider
  )

  result = await command.execute(LoginDto(
    login_credential= "nonexistentuser", 
    password= "12345")
  )

  assert result.is_error()
  assert result._error.code == "US-E-003" 
  assert result._error.message == "Invalid credentials"

@pytest.mark.asyncio
async def test_user_login_failure_invalid_password(id_generator, mock_publisher, temp_user_repository, token_provider, caesar_cypher_provider):
  
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload())
  
  assert result.is_success()

  command = LoginCommand(
    user_repository= temp_user_repository,
    token_provider= token_provider,
    cryptography_provider= caesar_cypher_provider
  )

  result = await command.execute(LoginDto(
    login_credential= "JohnDoe", 
    password= "IncorrectPassword")
  )

  assert result.is_error()
  assert result._error.code == "US-E-003" 
  assert result._error.message == "Invalid credentials"

@pytest.mark.asyncio
async def test_user_login_failure_user_suspended(id_generator, mock_publisher, temp_user_repository, temp_client_repository, temp_manager_repository, token_provider, caesar_cypher_provider):
  
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

  result = await command.execute(UpdateUserDto(id= user_id, status= UserStatus.SUSPENDED))

  assert result.is_success()

  command = LoginCommand(
    user_repository= temp_user_repository,
    token_provider= token_provider,
    cryptography_provider= caesar_cypher_provider
  )

  result = await command.execute(LoginDto(
    login_credential= "JohnDoe", 
    password= "password")
  )

  assert result.is_error()
  assert result._error.code == "US-E-UN" 
  assert result._error.message == "User suspended, please contact support"

import pytest
import asyncio
import pytest_asyncio

from src.user.application.commands.create.create_user_command import CreateUserCommand
from src.user.application.commands.delete_manager.delete_manager_command import DeleteManagerCommand
from tests.user.conftest import user_payload
from src.user.infrastructure.routes.types.create.create_user_dto import UserRole
from src.user.application.commands.delete_manager.types.dto import DeleteManagerDto
from src.user.infrastructure.models.postgres.sqlalchemy.user_model import UserStatus



@pytest.mark.asyncio
async def test_delete_manager_succesfully(id_generator, temp_user_repository, temp_manager_repository, mock_publisher, caesar_cypher_provider):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload(role= UserRole.MANAGER))
  
  assert result.is_success()
  manager_id = result.unwrap().user_id

  command = DeleteManagerCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(DeleteManagerDto(manager_id))

  assert result.is_success()
  assert result._info.code.value == "US-007"
  assert result._info.message == "User deleted succesfully"

  deleted_id = result.unwrap().id

  assert deleted_id == manager_id
  deleted_user = await temp_user_repository.find_one(manager_id)
  assert deleted_user != None
  assert deleted_user.status == UserStatus.SUSPENDED

  assert len(mock_publisher.events) == 2
  assert mock_publisher.events[1].name == "manager_suspended"


@pytest.mark.asyncio
async def test_delete_manager_failure_user_not_found(id_generator, temp_manager_repository, temp_user_repository, mock_publisher):
  command = DeleteManagerCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(DeleteManagerDto(id_generator.generate()))

  assert result.is_error()
  assert result._error.code == "US-E-NF" 
  assert result._error.message == "User not found"

@pytest.mark.asyncio
async def test_delete_manager_failure_user_is_not_manager(id_generator, temp_manager_repository, temp_user_repository, mock_publisher, caesar_cypher_provider):
  command = CreateUserCommand(
    id_generator= id_generator,
    user_repository= temp_user_repository,
    cryptography_provider= caesar_cypher_provider,
    event_publisher= mock_publisher
  )
  result = await command.execute(user_payload(role= UserRole.CLIENT))
  
  assert result.is_success()
  manager_id = result.unwrap().user_id

  command = DeleteManagerCommand(
    user_repository= temp_user_repository,
    manager_repository= temp_manager_repository,
    event_publisher= mock_publisher
  )

  result = await command.execute(DeleteManagerDto(manager_id))

  assert result.is_error()
  assert result._error.code == "US-E-005" 
  assert result._error.message == "User is not a manager"

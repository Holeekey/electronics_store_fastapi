import pytest
import asyncio
import pytest_asyncio
from src.common.domain.result.result import Result
from src.user.application.commands.create.create_user_command import CreateUserCommand


@pytest.mark.asyncio
async def test_create_user_succesfully(mock_user_repository, id_generator, caesar_cypher_provider,mock_publisher, client_payload):
  command = CreateUserCommand(id_generator= id_generator,
                              user_repository= mock_user_repository,
                              cryptography_provider= caesar_cypher_provider,
                              event_publisher= mock_publisher)
  result = await command.execute(client_payload)

  assert result.is_success
  assert result._info.code.value == "US-001"
  assert result._info.message == "User created successfully"





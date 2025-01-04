from uuid import UUID
from src.common.application.cryptography.cryptography_provider import ICryptographyProvider
from src.common.application.events.event_handlers import IEventPublisher
from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result
from src.common.domain.utils.is_none import is_none
from src.common.domain.utils.is_not_none import is_not_none
from src.user.application.commands.update.types.dto import UpdateUserDto
from src.user.application.commands.update.types.response import UpdateUserResponse
from src.user.application.info.user_updated_info import user_updated_info
from src.user.application.models.user import UserRole, UserStatus
from src.user.application.repositories.client_repository import IClientRepository
from src.user.application.repositories.manager_repository import IManagerRepository
from src.user.application.repositories.user_repository import IUserRepository
from src.user.application.errors.not_found import user_not_found_error
from src.user.application.errors.email_already_exists import email_already_exists_error
from src.user.application.errors.username_already_exists import username_already_exists_error
from src.user.application.errors.not_manager import user_is_not_manager_error
from src.user.application.errors.not_client import user_is_not_client_error
from src.user.application.errors.not_admin import user_is_not_admin_error
from src.user.domain.client.value_objects.client_email import ClientEmail
from src.user.domain.client.value_objects.client_id import ClientId
from src.user.domain.client.value_objects.client_name import ClientName
from src.user.domain.manager.value_objects.manager_email import ManagerEmail
from src.user.domain.manager.value_objects.manager_id import ManagerId
from src.user.domain.manager.value_objects.manager_name import ManagerName

class UpdateUserCommand(IApplicationService):
  def __init__(
      self, 
      user_repository: IUserRepository, 
      manager_repository: IManagerRepository,
      client_repository: IClientRepository,
      cryptography_provider: ICryptographyProvider,
      event_publisher: IEventPublisher,
    ):
    self.user_repository = user_repository
    self.manager_repository = manager_repository
    self.cryptography_provider = cryptography_provider
    self.event_publisher = event_publisher
    self.client_repository = client_repository

  async def execute(self, data: UpdateUserDto) -> Result[UpdateUserResponse]:
    user_to_update = await self.user_repository.find_one(data.id)
  
    if is_none(user_to_update):
      return Result.failure(error= user_not_found_error())

    manager = None
    client = None
    
    if is_not_none(data.role_to_update) and data.role_to_update.name != user_to_update.role.name:
      return Result.failure(
        user_is_not_manager_error() if data.role_to_update.name == UserRole.MANAGER.name
        else user_is_not_client_error() if data.role_to_update.name == UserRole.CLIENT.name
        else user_is_not_admin_error()
      )
    
    if user_to_update.role.name == UserRole.MANAGER.name:
      manager = await self.manager_repository.find_one(ManagerId(UUID(data.id)))
      manager.clear_events()
      
    if user_to_update.role.name == UserRole.CLIENT.name:
      client = await self.client_repository.find_one(ClientId(UUID(data.id)))
      client.clear_events()
    

    if is_not_none(data.email) and (data.email != user_to_update.email):
      if await self.user_repository.find_by_email(data.email):
        return Result.failure(error= email_already_exists_error())
      user_to_update.email = data.email
      if is_not_none(manager):
        manager.email = ManagerEmail(
          data.email
        )
      if is_not_none(client):
        client.email = ClientEmail(
          data.email
        )
      
    if is_not_none(data.username) and (data.username != user_to_update.username):
      if await self.user_repository.find_by_username(data.username):
        return Result.failure(error= username_already_exists_error())
      user_to_update.username = data.username
    
    if is_not_none(data.password):
      user_to_update.password = self.cryptography_provider.encrypt(data.password)

    if is_not_none(data.first_name):
      user_to_update.first_name = data.first_name

    if is_not_none(data.last_name):
      user_to_update.last_name = data.last_name
      
    if is_not_none(data.first_name) or is_not_none(data.last_name):
      if is_not_none(manager):
        manager.name = ManagerName(
          data.first_name if data.first_name else manager.name.first_name,
          data.last_name if data.last_name else manager.name.last_name 
        )
      if is_not_none(client):
        client.name = ClientName(
          data.first_name if data.first_name else client.name.first_name,
          data.last_name if data.last_name else client.name.last_name 
        )
      

    if is_not_none(data.status):
      previous_status = user_to_update.status
      user_to_update.status = data.status
      
      if data.status.name != previous_status.name:
        if data.status.name == UserStatus.ACTIVE.name:
          manager.activate() if is_not_none(manager) else client.activate()
        else:
          manager.suspend() if is_not_none(manager) else client.suspend()
      

    await self.user_repository.save(user_to_update)

    if is_not_none(manager):
      await self.event_publisher.publish(manager.pull_events())
      
    if is_not_none(client):
      await self.event_publisher.publish(client.pull_events())

    return Result.success(
      value= UpdateUserResponse(
        user_to_update.id,
        user_to_update.username,
        user_to_update.email,
        user_to_update.first_name,
        user_to_update.last_name,
        user_to_update.role,
        user_to_update.status
      ),
      info= user_updated_info()
    )
      
    

    
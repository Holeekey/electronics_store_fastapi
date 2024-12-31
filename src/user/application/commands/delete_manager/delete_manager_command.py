from uuid import UUID
from src.common.application.events.event_handlers import IEventPublisher
from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result
from src.common.domain.utils.is_none import is_none
from src.user.application.commands.delete_manager.types.dto import DeleteManagerDto
from src.user.application.commands.delete_manager.types.response import DeleteManagerResponse
from src.user.application.info.user_deleted_info import user_deleted_info
from src.user.application.models.user import UserRole, UserStatus
from src.user.application.repositories.manager_repository import IManagerRepository
from src.user.application.repositories.user_repository import IUserRepository
from src.user.application.errors.not_found import user_not_found_error
from src.user.application.errors.not_manager import user_is_not_manager_error
from src.user.application.errors.user_credentials_not_matching import user_credentials_not_matching_error
from src.user.domain.manager.value_objects.manager_id import ManagerId


class DeleteManagerCommand(IApplicationService):
  def __init__(
      self, 
      user_repository: IUserRepository, 
      manager_repository: IManagerRepository,
      event_publisher: IEventPublisher,
    ):
      self.user_repository = user_repository
      self.manager_repository = manager_repository
      self.event_publisher = event_publisher

  async def execute(self, data: DeleteManagerDto) -> Result[DeleteManagerResponse]:
    user = await self.user_repository.find_one(data.id)

    if is_none(user):
      return Result.failure(error= user_not_found_error())
    
    if user.role.name != UserRole.MANAGER.name:
      return Result.failure(error= user_is_not_manager_error()) 
    
    manager = await self.manager_repository.find_one(ManagerId(UUID(data.id)))
    
    manager.clear_events()
    
    user.status = UserStatus.SUSPENDED

    await self.user_repository.save(user)
    
    manager.suspend()
    
    await self.event_publisher.publish(manager.pull_events())
    
    return Result.success(
      value= DeleteManagerResponse(id= user.id),
      info= user_deleted_info()
    )
    
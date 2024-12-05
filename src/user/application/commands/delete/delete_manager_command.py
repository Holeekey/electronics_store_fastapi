from common.application.service.application_service import IApplicationService
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from user.application.commands.delete.types.dto import DeleteManagerDto
from user.application.commands.delete.types.response import DeleteManagerResponse
from user.application.info.user_deleted_info import user_deleted_info
from user.application.models.user import UserRole, UserStatus
from user.application.repositories.user_repository import IUserRepository
from user.application.errors.not_found import user_not_found_error
from user.application.errors.not_manager import user_is_not_manager_error
from user.application.errors.user_credentials_not_matching import user_credentials_not_matching_error


class DeleteManagerCommand(IApplicationService):
  def __init__(self, user_repository: IUserRepository):
    self.user_repository = user_repository

  async def execute(self, data: DeleteManagerDto) -> Result[DeleteManagerResponse]:
    manager = await self.user_repository.find_one(data.id)

    if is_none(manager):
      return Result.failure(error= user_not_found_error())
    
    if manager.role.name != UserRole.MANAGER.name:
      return Result.failure(error= user_is_not_manager_error()) 
    
    manager.status = UserStatus.SUSPENDED.name

    result = await self.user_repository.save(manager)
    
    return Result.success(
      value= DeleteManagerResponse(id= manager.id),
      info= user_deleted_info()
    )
    
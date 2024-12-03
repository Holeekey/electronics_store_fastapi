from common.application.service.application_service import IApplicationService
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from user.application.commands.delete.types.dto import DeleteManagerDto
from user.application.commands.delete.types.response import DeleteManagerResponse
from user.application.info.user_deleted_info import user_deleted_info
from user.application.models.user import UserRole
from user.application.repositories.user_repository import IUserRepository
from user.application.errors.not_found import user_not_found_error
from user.application.errors.user_credentials_not_matching import user_credentials_not_matching_error


class DeleteManagerCommand(IApplicationService):
  def __init__(self, user_repository: IUserRepository):
    self.user_repository = user_repository

  async def execute(self, data: DeleteManagerDto) -> Result[DeleteManagerResponse]:
    manager_to_delete = await self.user_repository.find_one(data.id)

    if is_none(manager_to_delete):
      return Result.failure(error= user_not_found_error())
    
    if manager_to_delete.role.name != UserRole.MANAGER.name:
      return Result.failure(error= user_credentials_not_matching_error()) 
    
    result = await self.user_repository.delete(data.id)

    if result.is_error:
      return result
    
    return Result.success(
      value= result.unwrap(),
      info= user_deleted_info()
    )
    
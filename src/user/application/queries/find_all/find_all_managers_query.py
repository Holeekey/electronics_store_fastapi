from typing import List
from common.application.service.application_service import IApplicationService
from common.domain.result.result import Result
from user.application.info.many_users_found_info import many_users_found_info
from user.application.models.user import UserRole
from user.application.queries.find_all.types.response import FindAllManagersResponse
from user.application.repositories.user_repository import IUserRepository

class FindAllManagersQuery(IApplicationService):
  
  def __init__(self, user_repository: IUserRepository):
    self.user_repository = user_repository

  async def execute(self, _) -> Result[List[FindAllManagersResponse]]:
    managers = await self.user_repository.find_by_role(UserRole.MANAGER)

    return Result.success([
      FindAllManagersResponse(
        manager.id,
        manager.username,
        manager.email,
        manager.first_name,
        manager.last_name,
        manager.role,
        manager.status
      )
      for manager in managers
    ], info= many_users_found_info()
    )
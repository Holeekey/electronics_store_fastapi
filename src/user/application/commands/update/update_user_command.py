from common.application.cryptography.cryptography_provider import ICryptographyProvider
from common.application.service.application_service import IApplicationService
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from common.domain.utils.is_not_none import is_not_none
from user.application.commands.update.types.dto import UpdateUserDto
from user.application.commands.update.types.response import UpdateUserResponse
from user.application.info.user_updated_info import user_updated_info
from user.application.repositories.user_repository import IUserRepository
from user.application.errors.not_found import user_not_found_error
from user.application.errors.email_already_exists import email_already_exists_error
from user.application.errors.username_already_exists import username_already_exists_error
from user.application.errors.user_credentials_not_matching import user_credentials_not_matching_error

class UpdateUserCommand(IApplicationService):
  def __init__(self, user_repository: IUserRepository, cryptography_provider: ICryptographyProvider):
    self.user_repository = user_repository
    self.cryptography_provider = cryptography_provider

  async def execute(self, data: UpdateUserDto) -> Result[UpdateUserResponse]:
    user_to_update = await self.user_repository.find_one(data.id)
  
    if is_none(user_to_update):
      return Result.failure(error= user_not_found_error())

    if user_to_update.role.name != data.current_role.name:
      return Result.failure(error= user_credentials_not_matching_error())

    if is_not_none(data.email) and (data.email != user_to_update.email):
      if await self.user_repository.find_by_email(data.email):
        return Result.failure(error= email_already_exists_error())
      
    if is_not_none(data.username) and (data.username != user_to_update.username):
      if await self.user_repository.find_by_username(data.username):
        return Result.failure(error= username_already_exists_error())
      user_to_update.username = data.username
    
    if is_not_none(data.password):
      user_to_update.password = self.cryptography_provider.encrypt(data.password)

    if is_not_none(data.email):
      user_to_update.email = data.email

    if is_not_none(data.first_name):
      user_to_update.first_name = data.first_name

    if is_not_none(data.last_name):
      user_to_update.last_name = data.last_name

    if is_not_none(data.new_role):
      user_to_update.role = data.new_role

    if is_not_none(data.status):
      user_to_update.status = data.status

    result = await self.user_repository.save(user_to_update)

    if result.is_error():
      return result

    updated_user = result.unwrap()

    return Result.success(
      value= UpdateUserResponse(
        updated_user.id,
        updated_user.username,
        updated_user.email,
        updated_user.first_name,
        updated_user.last_name,
        updated_user.role,
        updated_user.status
      ),
      info= user_updated_info()
    )
      
    

    
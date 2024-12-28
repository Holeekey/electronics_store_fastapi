from common.domain.result.result import result_info_factory
from user.application.info.codes.user_codes import UserCodes


user_updated_info = result_info_factory(
  code= UserCodes.UPDATED, message= "User updated successfully"
)
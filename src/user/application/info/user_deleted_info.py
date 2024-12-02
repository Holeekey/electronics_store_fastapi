from common.domain.result.result import result_info_factory
from user.application.info.codes.user_codes import UserCodes


user_deleted_info = result_info_factory(
  code= UserCodes.DELETED, message= "User deleted succesfully"
)
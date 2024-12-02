
from common.domain.result.result import result_info_factory
from user.application.info.codes.user_codes import UserCodes


many_users_found_info = result_info_factory(code=UserCodes.FIND_MANY, message="Users found succesfully")
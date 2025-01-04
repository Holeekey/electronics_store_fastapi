from src.common.domain.result.result import result_info_factory
from src.user.application.info.codes.user_codes import UserCodes


user_found_info = result_info_factory(
    code=UserCodes.FIND_ONE, message="User found successfully"
)

from src.common.domain.result.result import result_info_factory
from src.user.application.info.codes.user_codes import UserCodes


user_logged_in_info = result_info_factory(
    code=UserCodes.LOGIN, message="User logged in successfully"
)

from common.domain.result.result import result_info_factory
from user.application.info.codes.user_codes import UserCodes


current_user_info = result_info_factory(
        code=UserCodes.CURRENT, message="Current user found successfully"
    )
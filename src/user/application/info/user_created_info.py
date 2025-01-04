from src.common.domain.result.result import result_info_factory
from src.user.application.info.codes.user_codes import UserCodes


user_created_info = result_info_factory(
    code=UserCodes.CREATE, message="User created successfully"
)

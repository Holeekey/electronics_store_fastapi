from src.common.application.error.application_error import application_error_factory
from src.user.application.errors.codes.user_error_codes import UserErrorCodes

user_is_not_manager_error = application_error_factory(
    code=UserErrorCodes.NOT_MANAGER.value, message="User is not a manager"
)

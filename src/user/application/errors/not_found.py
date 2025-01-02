from src.common.application.error.application_error import application_error_factory
from src.user.application.errors.codes.user_error_codes import UserErrorCodes

user_not_found_error = application_error_factory(
    code=UserErrorCodes.NOT_FOUND.value, message="User not found"
)

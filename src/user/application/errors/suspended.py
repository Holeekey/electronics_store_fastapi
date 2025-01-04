from src.common.application.error.application_error import application_error_factory
from src.user.application.errors.codes.user_error_codes import UserErrorCodes

user_suspended_error = application_error_factory(
    code=UserErrorCodes.SUSPENDED.value,
    message="User suspended, please contact support",
)

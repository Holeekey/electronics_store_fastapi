from src.common.application.error.application_error import application_error_factory
from src.user.application.errors.codes.user_error_codes import UserErrorCodes

username_already_exists_error = application_error_factory(
    code=UserErrorCodes.USERNAME_ALREADY_EXISTS.value, message="Username already used"
)

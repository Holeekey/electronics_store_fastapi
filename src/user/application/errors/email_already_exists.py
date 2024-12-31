from src.common.application.error.application_error import (
    ApplicationError,
    application_error_factory,
)
from src.user.application.errors.codes.user_error_codes import UserErrorCodes

email_already_exists_error = application_error_factory(
    code=UserErrorCodes.EMAIL_ALREADY_EXISTS.value, message="Email already used"
)

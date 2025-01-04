from src.common.application.error.application_error import (
    ApplicationError,
    application_error_factory,
)
from src.user.application.errors.codes.user_error_codes import UserErrorCodes

invalid_credentials_error = application_error_factory(
    code=UserErrorCodes.INVALID_CREDENTIALS.value, message="Invalid credentials"
)

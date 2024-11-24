from common.application.error.application_error import (
    application_error_factory,
)

invalid_token_error = application_error_factory(
    code="JWT-E-001", message="Invalid token"
)

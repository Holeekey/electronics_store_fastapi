from common.application.error.application_error import (
    application_error_factory,
)

email_already_exists_error = application_error_factory(
    code='JWT-E-001', message="Invalid token"
)

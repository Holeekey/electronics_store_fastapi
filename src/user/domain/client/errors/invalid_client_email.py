from common.domain.error.domain_error import domain_error_factory

INVALID_CLIENT_EMAIL_ERROR = "invalid_client_email"

invalid_client_email_error = domain_error_factory(
    INVALID_CLIENT_EMAIL_ERROR, "Invalid client email format"
)

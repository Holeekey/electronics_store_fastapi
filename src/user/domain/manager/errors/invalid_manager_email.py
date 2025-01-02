from src.common.domain.error.domain_error import domain_error_factory

INVALID_MANAGER_EMAIL_ERROR = "invalid_manager_email"

invalid_manager_email_error = domain_error_factory(
    INVALID_MANAGER_EMAIL_ERROR, "Invalid manager email format"
)

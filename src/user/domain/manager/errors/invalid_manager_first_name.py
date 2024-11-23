from common.domain.error.domain_error import domain_error_factory

INVALID_MANAGER_FIRST_NAME_ERROR = "invalid_manager_first_name"

invalid_manager_first_name_error = domain_error_factory(
    INVALID_MANAGER_FIRST_NAME_ERROR,
    "First name length must be at least 1 character long",
)

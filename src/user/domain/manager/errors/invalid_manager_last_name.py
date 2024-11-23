from common.domain.error.domain_error import domain_error_factory

INVALID_MANAGER_LAST_NAME_ERROR = "invalid_manager_last_name"

invalid_manager_last_name_error = domain_error_factory(
    INVALID_MANAGER_LAST_NAME_ERROR,
    "Last name length must be at least 1 character long",
)

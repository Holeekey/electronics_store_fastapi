from common.domain.error.domain_error import domain_error_factory

INVALID_MANAGER_ID_ERROR = "invalid_manager_id"

invalid_manager_id_error = domain_error_factory(
    INVALID_MANAGER_ID_ERROR, "Invalid manager ID"
)

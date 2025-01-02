from src.common.domain.error.domain_error import domain_error_factory

INVALID_CLIENT_ID_ERROR = "invalid_client_id"

invalid_client_id_error = domain_error_factory(
    INVALID_CLIENT_ID_ERROR, "Invalid client ID"
)

from src.common.domain.error.domain_error import domain_error_factory

INVALID_CLIENT_LAST_NAME_ERROR = "invalid_product_name"

invalid_client_last_name_error = domain_error_factory(
    INVALID_CLIENT_LAST_NAME_ERROR,
    "Last name lenght must be at least 1 characters long",
)

from common.domain.error.domain_error import domain_error_factory

INVALID_CLIENT_FIRST_NAME_ERROR = "invalid_product_name"

invalid_client_first_name_error = domain_error_factory(
    INVALID_CLIENT_FIRST_NAME_ERROR,
    "First name lenght must be at least 1 characters long",
)

from src.common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_NAME_ERROR = "invalid_product_name"

invalid_product_name_error = domain_error_factory(
    INVALID_PRODUCT_NAME_ERROR, "Name must be at least 3 characters long"
)

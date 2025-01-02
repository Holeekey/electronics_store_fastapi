from common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_STATUS_ERROR = "invalid_status_value"

invalid_product_status_error = domain_error_factory(
    INVALID_PRODUCT_STATUS_ERROR, "Product status must be either active or inactive"
)

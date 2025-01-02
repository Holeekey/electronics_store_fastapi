from common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_ID_ERROR = "invalid_product_id"

invalid_product_id_error = domain_error_factory(
    INVALID_PRODUCT_ID_ERROR, "Invalid product ID"
)

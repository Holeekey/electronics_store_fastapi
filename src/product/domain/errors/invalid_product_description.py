from common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_DESCRIPTION_ERROR = "invalid_product_description"

invalid_product_description_error = domain_error_factory(
    INVALID_PRODUCT_DESCRIPTION_ERROR, "Description must be a string"
)

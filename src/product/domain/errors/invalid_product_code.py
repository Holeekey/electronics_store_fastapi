from src.common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_CODE_ERROR = "invalid_product_code"

invalid_product_code_error = domain_error_factory(
    INVALID_PRODUCT_CODE_ERROR, "Code must be non-empty"
)

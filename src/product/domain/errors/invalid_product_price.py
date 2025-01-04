from src.common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_PRICE_ERROR = "invalid_product_price"

invalid_product_price_error = domain_error_factory(
    INVALID_PRODUCT_PRICE_ERROR, "Prices start at 0.00"
)

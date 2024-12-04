from common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_PRICE_MARGIN_ERROR = "invalid_product_price_margin"

invalid_product_price_margin_error = domain_error_factory(
    INVALID_PRODUCT_PRICE_MARGIN_ERROR, "Earning margin must be higher than 0.00 and lower than 1.00"
)

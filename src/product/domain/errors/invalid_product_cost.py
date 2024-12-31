from src.common.domain.error.domain_error import domain_error_factory

INVALID_PRODUCT_COST_ERROR = "invalid_product_cost"

invalid_product_cost_error = domain_error_factory(
    INVALID_PRODUCT_COST_ERROR, "Cost must be higher than 0.00"
)

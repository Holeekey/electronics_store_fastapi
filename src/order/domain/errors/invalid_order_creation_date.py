from src.common.domain.error.domain_error import domain_error_factory

INVALID_ORDER_CREATION_DATE_ERROR = "invalid_creation_date_id"

invalid_order_creation_date_error = domain_error_factory(
    INVALID_ORDER_CREATION_DATE_ERROR, "Invalid order creation date"
)

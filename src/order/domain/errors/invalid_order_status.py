from src.common.domain.error.domain_error import domain_error_factory

INVALID_ORDER_STATUS_ERROR = "invalid_order_status"

invalid_order_status_error = domain_error_factory(
    INVALID_ORDER_STATUS_ERROR, "Invalid order status"
)

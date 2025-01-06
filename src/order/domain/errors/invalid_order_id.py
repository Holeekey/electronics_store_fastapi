from src.common.domain.error.domain_error import domain_error_factory

INVALID_ORDER_ID_ERROR = "invalid_order_id"

invalid_order_id_error = domain_error_factory(
    INVALID_ORDER_ID_ERROR, "Invalid order ID"
)

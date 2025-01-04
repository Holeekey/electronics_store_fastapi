from src.common.domain.error.domain_error import domain_error_factory

INVALID_ORDER_ITEM_PRICE_ERROR = "invalid_order_item_price"

invalid_order_item_price_error = domain_error_factory(
    INVALID_ORDER_ITEM_PRICE_ERROR, "Invalid order item price"
)

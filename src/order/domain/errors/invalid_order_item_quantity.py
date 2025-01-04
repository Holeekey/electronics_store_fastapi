from src.common.domain.error.domain_error import domain_error_factory

INVALID_ORDER_ITEM_QUANTITY_ERROR = "invalid_shopping_cart_id"

invalid_order_item_quantity_error = domain_error_factory(
    INVALID_ORDER_ITEM_QUANTITY_ERROR, "Order item quantity must be greater than zero (0)"
)

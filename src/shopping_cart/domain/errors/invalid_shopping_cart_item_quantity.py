from src.common.domain.error.domain_error import domain_error_factory

INVALID_SHOPPING_CART_ITEM_QUANTITY_ERROR = "invalid_shopping_cart_id"

invalid_shopping_cart_item_quantity_error = domain_error_factory(
    INVALID_SHOPPING_CART_ITEM_QUANTITY_ERROR, "Shopping cart item quantity must be greater than zero (0)"
)

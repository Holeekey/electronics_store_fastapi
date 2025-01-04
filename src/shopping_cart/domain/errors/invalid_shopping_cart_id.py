from src.common.domain.error.domain_error import domain_error_factory

INVALID_SHOPPING_CART_ID_ERROR = "invalid_shopping_cart_id"

invalid_shopping_cart_id_error = domain_error_factory(
    INVALID_SHOPPING_CART_ID_ERROR, "Invalid shopping cart ID"
)

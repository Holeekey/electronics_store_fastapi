from src.common.domain.error.domain_error import domain_error_factory

ITEM_IS_NOT_IN_SHOPPING_CART_ERROR = "invalid_shopping_cart_id"

item_is_not_in_shopping_cart_error = domain_error_factory(
    ITEM_IS_NOT_IN_SHOPPING_CART_ERROR, "Item is not in shopping cart"
)

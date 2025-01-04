from src.order.application.errors.codes.order_error_codes import OrderErrorCodes
from src.common.application.error.application_error import application_error_factory

shopping_cart_empty_error = application_error_factory(
    code=OrderErrorCodes.SHOPPING_CART_EMPTY.value, message="Shopping cart is empty"
)

from src.shopping_cart.application.errors.codes.shopping_cart_error_codes import ShoppingCartErrorCodes
from src.common.application.error.application_error import application_error_factory

shopping_cart_not_found_error = application_error_factory(
    code=ShoppingCartErrorCodes.NOT_FOUND.value, message="Shopping cart not found"
)

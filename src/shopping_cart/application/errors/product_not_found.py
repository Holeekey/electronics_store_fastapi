from src.shopping_cart.application.errors.codes.shopping_cart_error_codes import ShoppingCartErrorCodes
from src.common.application.error.application_error import application_error_factory

product_not_found_error = application_error_factory(
    code=ShoppingCartErrorCodes.PRODUCT_NOT_FOUND.value, message="Product not found"
)

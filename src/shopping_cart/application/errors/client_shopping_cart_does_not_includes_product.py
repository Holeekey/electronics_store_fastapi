from src.shopping_cart.application.errors.codes.shopping_cart_error_codes import ShoppingCartErrorCodes
from src.common.application.error.application_error import application_error_factory

client_shopping_cart_does_not_includes_product_error = application_error_factory(
    code=ShoppingCartErrorCodes.CLIENT_SHOPPING_CART_DOES_NOT_INCLUDES_PRODUCT.value, message="Client's shopping cart does not include the product"
)

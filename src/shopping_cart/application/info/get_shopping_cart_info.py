from src.shopping_cart.application.info.codes.shopping_cart_codes import ShoppingCartCodes
from src.common.domain.result.result import result_info_factory



get_shopping_cart_info = result_info_factory(
    code=ShoppingCartCodes.FOUND, message="Shopping cart found successfully"
)

from src.shopping_cart.application.info.codes.shopping_cart_codes import ShoppingCartCodes
from src.common.domain.result.result import result_info_factory



add_items_to_shopping_cart_info = result_info_factory(
    code=ShoppingCartCodes.ADD_ITEMS.value, message="Items added to shopping cart successfully"
)

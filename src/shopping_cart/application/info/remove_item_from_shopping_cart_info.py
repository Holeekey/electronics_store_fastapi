from src.shopping_cart.application.info.codes.shopping_cart_codes import ShoppingCartCodes
from src.common.domain.result.result import result_info_factory



remove_item_from_shopping_cart_info = result_info_factory(
    code=ShoppingCartCodes.REMOVE_ITEM.value, message="Item removed from shopping cart successfully"
)

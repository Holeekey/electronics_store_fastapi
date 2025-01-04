from src.product.domain.value_objects.product_id import ProductId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.shopping_cart.domain.value_objects.shopping_cart_item_quantity import ShoppingCartItemQuantity


def shopping_cart_item_factory(product_id: str, quantity: int) -> ShoppingCartItem:
    return ShoppingCartItem(
        product_id= ProductId(product_id), 
        quantity= ShoppingCartItemQuantity(quantity)
    )
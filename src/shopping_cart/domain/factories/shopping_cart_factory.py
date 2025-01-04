from uuid import UUID

from src.shopping_cart.domain.shopping_cart import ShoppingCart
from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.user.domain.client.value_objects.client_id import ClientId



def shopping_cart_factory(
    id: UUID,
    client_id: str,
    items: list[ShoppingCartItem]
):
    return ShoppingCart(
        ShoppingCartId(UUID(id)),
        ClientId(UUID(client_id)),
        items
    )
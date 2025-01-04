from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.common.domain.events.domain_event import DomainEvent
from src.user.domain.client.value_objects.client_id import ClientId


SHOPPING_CART_ITEMS_ADDED = "shopping_cart_items_added"

class ShoppingCartItemsAdded(DomainEvent):
    def __init__(self, id: ShoppingCartId, client_id: ClientId, items: list[ShoppingCartItem]):
        super().__init__(SHOPPING_CART_ITEMS_ADDED)
        self.id = id
        self.client_id = client_id
        self.items = items

from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.common.domain.events.domain_event import DomainEvent


SHOPPING_CART_ITEMS_ADDED = "shopping_cart_items_added"

class ShoppingCartItemsAdded(DomainEvent):
    def __init__(self, id: ShoppingCartId, items: list[ShoppingCartItem]):
        super().__init__(SHOPPING_CART_ITEMS_ADDED)
        self.id = id
        self.items = items

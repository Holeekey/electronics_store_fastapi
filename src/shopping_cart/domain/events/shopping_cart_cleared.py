from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.common.domain.events.domain_event import DomainEvent
from src.user.domain.client.value_objects.client_id import ClientId


SHOPPING_CART_CLEARED = "shopping_cart_cleared"

class ShoppingCartCleared(DomainEvent):
    def __init__(self, id: ShoppingCartId, client_id: ClientId):
        super().__init__(SHOPPING_CART_CLEARED)
        self.id = id
        self.client_id = client_id

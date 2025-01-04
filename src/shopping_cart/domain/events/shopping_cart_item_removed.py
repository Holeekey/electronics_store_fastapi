from src.product.domain.value_objects.product_id import ProductId
from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.common.domain.events.domain_event import DomainEvent
from src.user.domain.client.value_objects.client_id import ClientId


SHOPPING_CART_ITEM_REMOVED = "shopping_cart_item_removed"

class ShoppingCartItemRemoved(DomainEvent):
    def __init__(self, id: ShoppingCartId, client_id: ClientId, product_id: ProductId):
        super().__init__(SHOPPING_CART_ITEM_REMOVED)
        self.id = id
        self.client_id = client_id
        self.product_id = product_id

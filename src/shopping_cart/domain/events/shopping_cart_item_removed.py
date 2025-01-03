from src.product.domain.value_objects.product_id import ProductId
from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.common.domain.events.domain_event import DomainEvent


SHOPPING_CART_ITEM_REMOVED = "shopping_cart_item_removed"

class ShoppingCartItemRemoved(DomainEvent):
    def __init__(self, id: ShoppingCartId, product_id: ProductId):
        super().__init__(SHOPPING_CART_ITEM_REMOVED)
        self.id = id
        self.product_id = product_id

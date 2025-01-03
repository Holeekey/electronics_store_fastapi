from typing import TypeVar

from shopping_cart.domain.events.shopping_cart_cleared import ShoppingCartCleared
from src.shopping_cart.domain.events.shopping_cart_item_removed import ShoppingCartItemRemoved
from src.shopping_cart.domain.events.shopping_cart_items_added import ShoppingCartItemsAdded
from src.common.domain.utils.is_none import is_none
from src.product.domain.value_objects.product_id import ProductId
from src.shopping_cart.domain.value_objects.shopping_cart_item import ShoppingCartItem
from src.common.domain.aggregate.aggregate import Aggregate
from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.user.domain.client.value_objects.client_id import ClientId
from src.shopping_cart.domain.errors.item_is_not_in_shopping_cart import item_is_not_in_shopping_cart_error

T = TypeVar("T", bound=ShoppingCartId)


class ShoppingCart(Aggregate[T]):
    def __init__(
        self,
        id: ShoppingCartId,
        client_id: ClientId,
        items: list[ShoppingCartItem] = []
    ) -> None:
        super().__init__(id)
        self._client_id = client_id
        self._items = items
    
    @property
    def items(self) -> list[ShoppingCartItem]:
        return self._items
        
    def add_items(self, items: list[ShoppingCartItem]):
        for item_to_add in items:
            item_found = None
            for item in self._items:
                if item.product_id == item_to_add.product_id:
                    item_found = item
                    break
            if item_found:
                item_found_index = self._items.index(item_found)
                self._items.pop(item_found_index)
            self._items.append(item)
            
        self.publish(ShoppingCartItemsAdded(
            self._id,
            self._items,
        ))
    
    def remove_item(self, product_id: ProductId):
        item_found = None
        for item in self._items:
            if item.product_id == product_id:
                item_found = item
                break
        
        if is_none(item_found):
            raise item_is_not_in_shopping_cart_error(
                {
                    "product_id": product_id.id
                }
            )
        
        self._items.pop(self._items.index(item_found))
        self.publish(ShoppingCartItemRemoved(
            self._id,
            product_id,
        ))
    
    def clear_items(self):
        self._items.clear()
        self.publish(ShoppingCartCleared(
            self._id
        ))
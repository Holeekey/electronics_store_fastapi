from abc import ABCMeta, abstractmethod
from typing import Optional

from src.shopping_cart.domain.shopping_cart import ShoppingCart
from src.user.domain.client.value_objects.client_id import ClientId


class IShoppingCartRepository(metaclass=ABCMeta):

    @abstractmethod
    async def find_by_client_id(self, client_id: ClientId) -> Optional[ShoppingCart]:
        pass
    
    @abstractmethod
    async def save(self, shopping_cart: ShoppingCart) -> None:
        pass
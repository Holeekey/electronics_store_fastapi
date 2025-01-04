from abc import ABCMeta, abstractmethod
from typing import Optional

from src.common.domain.result.result import Result
from src.inventory.domain.inventory import Inventory
from src.product.domain.value_objects.product_id import ProductId



class IInventoryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def find_by_product_id(self, product_id:ProductId) -> Optional[Inventory]:
        pass

    @abstractmethod
    async def update(self, inventory: Inventory) -> Result[Inventory]:
        pass

    @abstractmethod
    async def save(self, inventory:Inventory) -> Result[Inventory]:
        pass
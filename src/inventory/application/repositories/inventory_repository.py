from abc import ABCMeta, abstractmethod
from typing import Optional

from common.domain.result.result import Result
from inventory.domain.inventory import Inventory
from product.domain.value_objects.product_id import Product_id



class IInventoryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def find_by_product_id(self, product_id:Product_id) -> Optional[Inventory]:
        pass

    @abstractmethod
    async def save(self, inventory:Inventory) -> Result[Inventory]:
        pass
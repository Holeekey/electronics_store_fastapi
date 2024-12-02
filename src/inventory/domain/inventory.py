from typing import TypeVar
from common.domain.entity.entity import Entity
from inventory.domain.events.inventory_created import InventoryCreated
from inventory.domain.value_objects.inventory_id import InventoryId
from inventory.domain.value_objects.inventory_stock import Stock
from product.domain.product import ProductId

T = TypeVar("T", bound=InventoryId)


class Inventory(Entity[T]):
    def __init__(self, id: InventoryId, stock:Stock, product_id:ProductId):
        super().__init__(id)
        self._stock = stock
        self._product_id = product_id
        self.publish(InventoryCreated(id, stock,product_id))

    @property
    def id(self) -> Stock:
        return self._stock
    
    @property
    def id(self) -> ProductId:
        return self._product_id
    
    def __eq__(self, other: 'Inventory') -> bool:
        return self._id.equals(other.id)
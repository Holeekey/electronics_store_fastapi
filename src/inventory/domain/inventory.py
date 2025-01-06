from typing import TypeVar
from src.common.domain.entity.entity import Entity
from src.inventory.domain.value_objects.inventory_id import InventoryId
from src.inventory.domain.value_objects.inventory_stock import Stock
from src.product.domain.value_objects.product_id import ProductId

T = TypeVar("T", bound=InventoryId)


class Inventory(Entity[T]):
    def __init__(self, id: InventoryId, stock:Stock, product_id:ProductId):
        super().__init__(id)
        self._stock = stock
        self._product_id = product_id

    @property
    def stock(self) -> Stock:
        return self._stock
    
    @stock.setter
    def stock(self, stock: Stock) -> None:
        self._stock = stock
    
    @property
    def product_id(self) -> ProductId:
        return self._product_id
    
    def __eq__(self, other: 'Inventory') -> bool:
        return self._id == other.id

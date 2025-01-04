from uuid import UUID

from src.inventory.domain.inventory import Inventory
from src.inventory.domain.value_objects.inventory_id import InventoryId
from src.inventory.domain.value_objects.inventory_stock import Stock
from src.product.domain.value_objects.product_id import ProductId



def inventory_factory(id: UUID, stock: int, product_id: str):

    product_id_vo = ProductId(product_id)
    inventory_id = InventoryId(id)
    inventory_stock = Stock(stock)

    return Inventory(inventory_id, inventory_stock, product_id_vo)

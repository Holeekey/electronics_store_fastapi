from uuid import UUID

from inventory.domain.inventory import Inventory
from inventory.domain.value_objects.inventory_id import InventoryId
from inventory.domain.value_objects.inventory_stock import Stock
from product.domain.value_objects.product_id import ProductId



def inventory_factory(id: UUID, stock: int, product_id: str):

    product_id_vo = ProductId(product_id)
    inventory_id = InventoryId(id)
    inventory_stock = Stock(stock)

    return Inventory(inventory_id, inventory_stock, product_id_vo)

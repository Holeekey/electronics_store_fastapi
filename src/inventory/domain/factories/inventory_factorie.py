from uuid import UUID

from inventory.domain.inventory import Inventory
from inventory.domain.value_objects.inventory_id import InventoryId
from inventory.domain.value_objects.inventory_stock import Stock
from product.domain.product import ProductId



def inventory_factory(id: UUID, stock: int):

    inventory_id = InventoryId(id)
    inventory_stock = Stock(stock)
    product_id = ProductId(id)

    return Inventory(inventory_id, inventory_stock,product_id)

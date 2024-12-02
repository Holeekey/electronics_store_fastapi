from common.domain.events.domain_event import DomainEvent
from inventory.domain.value_objects.inventory_id import InventoryId
from inventory.domain.value_objects.inventory_stock import InventoryStock
from product.domain.product import ProductId

INVENTORY_CREATED = "inventory_created"


class InventoryCreated(DomainEvent):
    def __init__(self, inventory_id: InventoryId, stock: InventoryStock, product_id: ProductId):
        super().__init__(INVENTORY_CREATED)
        self.inventory_id = inventory_id
        self.inventory_stock = stock
        self.product_id = product_id

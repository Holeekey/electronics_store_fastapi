from common.domain.events.domain_event import DomainEvent
from inventory.domain.value_objects.inventory_id import InventoryId
from inventory.domain.value_objects.inventory_stock import Stock
from product.domain.value_objects.product_id import ProductId

INVENTORY_CREATED = "inventory_created"


class InventoryCreated(DomainEvent):
    def __init__(self, inventory_id: InventoryId, stock: Stock, product_id: ProductId):
        super().__init__(INVENTORY_CREATED)
        self.inventory_id = inventory_id
        self.stock = stock
        self.product_id = product_id

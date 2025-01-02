from typing import List
from inventory.application.models.inventory import Inventory
from inventory.application.repositories.inventory_repository import IInventoryRepository


class InventoryRepositoryMock(IInventoryRepository):

    inventories: List[Inventory]

    def __init__(self):
        self.inventories = []

    async def find_by_product_id(self, id: str):
        for inventory in self.inventories:
            if inventory.product_id == str:
                return inventory
        return None


    async def save(self, inventory: Inventory):
        self.inventories.append(inventory)
        return inventory

from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from common.infrastructure.database.database import SessionLocal
from inventory.application.info.inventory_created_info import inventory_created_info
from inventory.application.info.inventory_updated_info import inventory_updated_info
from inventory.application.errors.not_found import inventory_not_found_error
from inventory.application.models.inventory import Inventory
from inventory.application.repositories.inventory_repository import IInventoryRepository
from inventory.infrastructure.models.postgres.sqlalchemy.inventory_model import InventoryModel
from sqlalchemy.orm import Session
from product.domain.value_objects.product_id import ProductId


class InventoryRepositorySqlAlchemy(IInventoryRepository):
    def __init__(self, db:Session):
        self.db = db

    def map_model_to_inventory(self, inventory_orm: InventoryModel) -> Inventory:
        return Inventory(
            id=inventory_orm.id,
            product_id=inventory_orm.product_id,
            stock=inventory_orm.stock,
        )

    async def find_by_product_id(self, product_id: str):
        inventory_orm =(self.db.query(InventoryModel).filter(InventoryModel.product_id == product_id))
        if is_none(inventory_orm):
            return None
        return self.map_model_to_inventory(inventory_orm)

    async def update(self, inventory: Inventory) -> Result[Inventory]:
        inventory_orm = (self.db.query(InventoryModel).filter(InventoryModel.product_id == inventory.product_id))
        if is_none(inventory_orm):
            return Result.failure(error=inventory_not_found_error)

        inventory_orm.stock = inventory.stock
        await self.db.commit()
        await self.db.refresh(inventory_orm)
        return Result.success(inventory, info=inventory_updated_info)

    async def save(self, inventory: Inventory) -> Result[Inventory]:
        inventory_orm = InventoryModel(
            id=inventory.id,
            product_id=inventory.product_id,
            stock=inventory.stock,
        )
        self.db.add(inventory_orm)
        await self.db.commit()
        await self.db.refresh(inventory_orm)
        return Result.success(inventory, info=inventory_created_info)

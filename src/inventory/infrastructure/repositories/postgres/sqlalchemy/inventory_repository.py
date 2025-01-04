from uuid import UUID
from src.common.domain.result.result import Result
from src.common.domain.utils.is_none import is_none
from src.common.infrastructure.database.database import SessionLocal
from src.inventory.application.info.inventory_created_info import inventory_created_info
from src.inventory.application.info.inventory_updated_info import inventory_updated_info
from src.inventory.application.errors.not_found import inventory_not_found_error
from src.inventory.domain.factories.inventory_factory import inventory_factory
from src.inventory.domain.inventory import Inventory
from src.inventory.application.repositories.inventory_repository import IInventoryRepository
from src.inventory.infrastructure.models.postgres.sqlalchemy.inventory_model import InventoryModel
from sqlalchemy.orm import Session
from src.product.domain.value_objects.product_id import ProductId


class InventoryRepositorySqlAlchemy(IInventoryRepository):
    def __init__(self, db:Session):
        self.db = db

    def map_model_to_inventory(self, inventory_orm: InventoryModel) -> Inventory:
        
        inventory:Inventory = inventory_factory(
            id=UUID(inventory_orm.id),
            product_id=inventory_orm.product_id,
            stock=inventory_orm.stock,
        )
        
        return inventory

    async def find_by_product_id(self, product_id: ProductId):
        inventory_orm =(self.db.query(InventoryModel).filter(InventoryModel.product_id == str(product_id.id))).first()
        if is_none(inventory_orm):
            return None
        return self.map_model_to_inventory(inventory_orm)

    async def update(self, inventory: Inventory) -> Result[Inventory]:
        inventory_orm = (self.db.query(InventoryModel).filter(InventoryModel.product_id == inventory.product_id))
        if is_none(inventory_orm):
            return Result.failure(error=inventory_not_found_error)

        inventory_orm.stock = inventory.stock
        self.db.commit()
        self.db.refresh(inventory_orm)
        return Result.success(inventory, info=inventory_updated_info)

    async def save(self, inventory: Inventory) -> Result[Inventory]:
        
        inventory_orm =(self.db.query(InventoryModel).filter(InventoryModel.product_id == str(inventory.product_id.id))).first()
        
        if is_none(inventory_orm):
            inventory_orm = InventoryModel(
                id=inventory.id.id,
                product_id=inventory.product_id.id,
                stock=inventory.stock.value,
            )
        else:
            inventory_orm.stock = inventory.stock.value
        self.db.add(inventory_orm)
        self.db.commit()
        self.db.refresh(inventory_orm)
        return Result.success(inventory, info=inventory_created_info)

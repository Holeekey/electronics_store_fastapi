from uuid import UUID
from src.inventory.application.errors.product_does_not_exist import product_does_not_exist
from src.common.domain.utils.is_none import is_none
from src.product.application.repositories.product_repository import IProductRepository
from src.common.application.id_generator.id_generator import IDGenerator
from src.common.domain.result.result import Result
from src.common.application.service.application_service import IApplicationService
from src.inventory.application.commands.types.adjust_inventory_dto import AdjustInventoryDto
from src.inventory.application.commands.types.response import CreateInventoryResponse
from src.inventory.application.errors import negative_stock
from src.inventory.application.info.inventory_updated_info import inventory_updated_info
from src.inventory.application.repositories.inventory_repository import IInventoryRepository
from src.inventory.application.info.inventory_created_info import inventory_created_info
from src.inventory.domain.factories.inventory_factory import inventory_factory
from src.inventory.domain.inventory import Inventory
from src.inventory.domain.value_objects.inventory_stock import Stock
from src.product.domain.value_objects.product_id import ProductId


class AdjustInventoryCommand(IApplicationService):

    def __init__(self, id_generator: IDGenerator, inventory_repository: IInventoryRepository, product_repository: IProductRepository):
        self._inventory_repository = inventory_repository
        self._id_generator = id_generator
        self._product_repository = product_repository

    async def execute(self, data: AdjustInventoryDto) -> Result[CreateInventoryResponse]:
        # Buscar el inventario existente por product_id
        existing_inventory = await self._inventory_repository.find_by_product_id(product_id=ProductId(str(data.product_id)))

        if existing_inventory:
            # Ajustar el stock del inventario existente
            existing_inventory.stock = Stock(existing_inventory.stock.value + data.stock_change)

            if existing_inventory.stock.value < 0:
                return Result.failure(error=negative_stock())

            await self._inventory_repository.save(existing_inventory)
            return Result.success(
                value=CreateInventoryResponse(id=existing_inventory.id),
                info=inventory_updated_info()
            )
        
        #Chequear que el producto exista
        product = await self._product_repository.find_one(ProductId(data.product_id))

        if is_none(product):
            return Result.failure(error= product_does_not_exist())
        
        # Crear un nuevo inventario si no existe
        initial_stock = max(0, data.stock_change)  # El stock inicial no puede ser negativo

        inventory:Inventory = inventory_factory(
            id=UUID(self._id_generator.generate()),
            product_id=str(data.product_id),
            stock=initial_stock,
        )

        await self._inventory_repository.save(inventory=inventory)

        return Result.success(
            value=CreateInventoryResponse(id=inventory.id),
            info=inventory_created_info()
        )

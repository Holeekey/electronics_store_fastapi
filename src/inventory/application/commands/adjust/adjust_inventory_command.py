from uuid import UUID
from common.application.id_generator.id_generator import IDGenerator
from common.domain.result.result import Result
from common.application.service.application_service import IApplicationService
from inventory.application.commands.types.adjust_inventory_dto import AdjustInventoryDto
from inventory.application.commands.types.response import CreateInventoryResponse
from inventory.application.errors import negative_stock
from inventory.application.info.inventory_updated_info import inventory_updated_info
from inventory.application.repositories.inventory_repository import IInventoryRepository
from inventory.application.info.inventory_created_info import inventory_created_info
from inventory.domain.factories.inventory_factory import inventory_factory
from inventory.domain.inventory import Inventory
from inventory.domain.value_objects.inventory_stock import Stock
from product.domain.value_objects.product_id import ProductId


class AdjustInventoryCommand(IApplicationService):

    def __init__(self, id_generator: IDGenerator, inventory_repository: IInventoryRepository):
        self._inventory_repository = inventory_repository
        self._id_generator = id_generator

    async def execute(self, data: AdjustInventoryDto) -> Result[CreateInventoryResponse]:
        # Buscar el inventario existente por product_id
        existing_inventory = await self._inventory_repository.find_by_product_id(product_id=ProductId(str(data.product_id)))

        if existing_inventory:
            # Ajustar el stock del inventario existente
            existing_inventory.stock = Stock(existing_inventory.stock.value + data.stock)

            if existing_inventory.stock.value < 0:
                return Result.failure(error=negative_stock())

            await self._inventory_repository.save(existing_inventory)
            return Result.success(
                value=CreateInventoryResponse(id=existing_inventory.id),
                info=inventory_updated_info()
            )

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

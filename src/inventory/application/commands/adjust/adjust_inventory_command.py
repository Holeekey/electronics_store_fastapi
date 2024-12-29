from common.application.id_generator.id_generator import IDGenerator
from common.domain.result.result import Result
from common.application.service.application_service import IApplicationService
from inventory.application.commands.types.adjustInventoryDto import AdjustInventoryDto
from inventory.application.commands.types.response import AdjustInventoryResponse
from inventory.application.errors import negative_stock
from inventory.application.info import inventory_updated_info
from inventory.application.repositories.inventory_repository import IInventoryRepository
from inventory.application.info.inventory_created_info import inventory_created_info
from inventory.application.models.inventory import Inventory


class AdjustInventoryCommand(IApplicationService):

    def __init__(self, id_generator: IDGenerator, inventory_repository: IInventoryRepository):
        self._inventory_repository = inventory_repository
        self._id_generator = id_generator

    async def execute(self, data: AdjustInventoryDto) -> Result[AdjustInventoryResponse]:
        # Buscar el inventario existente por product_id
        existing_inventory = await self._inventory_repository.find_by_product_id(product_id=data.product_id)

        if existing_inventory:
            # Ajustar el stock del inventario existente
            existing_inventory.stock += data.stock_change

            if existing_inventory.stock < 0:
                return Result.failure(error=negative_stock())

            await self._inventory_repository.update(existing_inventory)
            return Result.success(
                value=AdjustInventoryResponse(id=existing_inventory.id),
                info=inventory_updated_info()
            )

        # Crear un nuevo inventario si no existe
        initial_stock = max(0, data.stock_change)  # El stock inicial no puede ser negativo
        inventory = Inventory(
            id=self._id_generator.generate(),
            product_id=data.product_id,
            stock=initial_stock,
        )

        await self._inventory_repository.save(inventory=inventory)

        return Result.success(
            value=AdjustInventoryResponse(id=inventory.id),
            info=inventory_created_info()
        )

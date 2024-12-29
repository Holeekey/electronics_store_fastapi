from common.application.id_generator.id_generator import IDGenerator
from common.domain.result.result import Result
from common.application.service.application_service import IApplicationService
from inventory.application.commands.types.createInventorydto import CreateInventoryDto
from inventory.application.commands.types.response import CreateInventoryResponse
from inventory.application.info import inventory_updated_info
from inventory.application.repositories.inventory_repository import IInventoryRepository
from inventory.application.info.inventory_created_info import inventory_created_info
from inventory.application.models.inventory import Inventory


class CreateOrUpdateInventoryCommand(IApplicationService):

    def __init__(self, id_generator: IDGenerator, inventory_repository: IInventoryRepository):
        self._inventory_repository = inventory_repository
        self._id_generator = id_generator

    async def execute(self, data: CreateInventoryDto) -> Result[CreateInventoryResponse]:

        existing_inventory = await self._inventory_repository.find_by_product_id(product_id=data.product_id)

        if existing_inventory:
            # Actualizar el stock completo si el inventario ya existe
            existing_inventory.stock = data.stock
            await self._inventory_repository.update(existing_inventory)
            return Result.success(
                value=CreateInventoryResponse(id=existing_inventory.id),
                info=inventory_updated_info()
            )

        # Crear un nuevo inventario si no existe
        inventory = Inventory(
            id=self._id_generator.generate(),
            product_id=data.product_id,
            stock=data.stock,
        )

        await self._inventory_repository.save(inventory=inventory)

        return Result.success(
            value=CreateInventoryResponse(id=inventory.id), info=inventory_created_info()
        )

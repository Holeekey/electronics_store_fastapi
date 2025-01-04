from uuid import UUID
from src.common.application.id_generator.id_generator import IDGenerator
from src.common.domain.result.result import Result
from src.common.application.service.application_service import IApplicationService
from src.inventory.application.commands.types.create_inventory_dto import CreateInventoryDto
from src.inventory.application.commands.types.response import CreateInventoryResponse
from src.inventory.application.info.inventory_updated_info import inventory_updated_info
from src.inventory.application.repositories.inventory_repository import IInventoryRepository
from src.inventory.application.info.inventory_created_info import inventory_created_info
from src.inventory.domain.factories.inventory_factory import inventory_factory
from src.inventory.domain.inventory import Inventory
from src.inventory.domain.value_objects.inventory_stock import Stock
from src.product.domain.value_objects.product_id import ProductId


class CreateOrUpdateInventoryCommand(IApplicationService):

    def __init__(self, id_generator: IDGenerator, inventory_repository: IInventoryRepository):
        self._inventory_repository = inventory_repository
        self._id_generator = id_generator

    async def execute(self, data: CreateInventoryDto) -> Result[CreateInventoryResponse]:

        existing_inventory = await self._inventory_repository.find_by_product_id(product_id=ProductId(str(data.product_id)))

        if existing_inventory:
            # Actualizar el stock completo si el inventario ya existe
            existing_inventory.stock = Stock(data.stock)
            await self._inventory_repository.save(existing_inventory)
            return Result.success(
                value=CreateInventoryResponse(id=existing_inventory.id),
                info=inventory_updated_info()
            )

        # Crear un nuevo inventario si no existe
        
        id = self._id_generator.generate()

        inventory:Inventory = inventory_factory(
            id=UUID(id),
            product_id=str(data.product_id),
            stock=data.stock,
        )

        await self._inventory_repository.save(inventory=inventory)

        return Result.success(
            value=CreateInventoryResponse(id=inventory.id), info=inventory_created_info()
        )

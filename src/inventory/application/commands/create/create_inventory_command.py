from common.application.id_generator.id_generator import IDGenerator
from common.domain.result.result import Result
from common.application.service.application_service import IApplicationService
from inventory.application.commands.create.types.dto import CreateInventoryDto
from inventory.application.commands.create.types.response import CreateInventoryResponse
from inventory.application.repositories.inventory_repository import IInventoryRepository
from inventory.application.info.inventory_created_info import inventory_created_info
from inventory.application.models.inventory import Inventory
from inventory.application.errors.inventory_already_exists import (
    inventory_already_exists_error,
)


class CreateUserCommand(IApplicationService):

    def __init__(self, id_generator: IDGenerator, inventory_repository: IInventoryRepository):
        self._user_repository = inventory_repository
        self._id_generator = id_generator

    async def execute(self, data: CreateInventoryDto) -> Result[CreateInventoryResponse]:

        if await self._inventory_repository.find_by_product_id(productId=data.productId):
            return Result.failure(error=inventory_already_exists_error())


        inventory = Inventory(
            id=self._id_generator.generate(),
            productId=data.productId,
            stock=data.stock,
        )

        await self._inventory_repository.save(inventory=inventory)

        return Result.success(
            value=CreateInventoryResponse(id=inventory.id), info=inventory_created_info()
        )

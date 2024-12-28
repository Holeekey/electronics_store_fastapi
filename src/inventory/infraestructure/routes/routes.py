from uuid import UUID
from fastapi import APIRouter

from common.application.decorators.error_decorator import ErrorDecorator
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from inventory.application.commands.create.create_inventory_command import (
    CreateInventoryCommand,
)
from inventory.application.queries.find_one_product_query import (
    FindOneProductQuery,
)
from inventory.application.queries import FindOneInventoryDto
from inventory.infraestructure.repositories.postgres.sqlalchemy.inventory_repository import (
    InventoryRepositorySqlAlchemy,
)
from inventory.infraestructure.routes.types.dto.create.create_inventory_dto import CreateInventoryDto


inventory_router = APIRouter(
    prefix="/inventories",
    tags=["Inventory"],
    responses={404: {"description": "Not found"}},
)

inventory_repository = InventoryRepositorySqlAlchemy()


@inventory_router.get("/{product_id}")
async def find_inventory_by_product(id: UUID):

    result = await ErrorDecorator(
        service=FindOneProductQuery(inventory_repository=inventory_repository),
        error_handler=error_response_handler,
    ).execute(data=FindOneInventoryDto(id=id.__str__()))

    return result.handle_success(handler=success_response_handler)


@inventory_router.post("/{product_id}")
async def create_inventory(body: CreateInventoryDto):

    # idGenerator = RandomIdGenerator()
    idGenerator = UUIDGenerator()

    result = await ErrorDecorator(
        service=CreateInventoryCommand(
            id_generator=idGenerator, product_repository=inventory_repository
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)

@inventory_router.put("/{product_id}")
async def update_inventory(body: CreateInventoryDto):

    # idGenerator = RandomIdGenerator()
    idGenerator = UUIDGenerator()

    result = await ErrorDecorator(
        service=CreateInventoryCommand(
            id_generator=idGenerator, product_repository=inventory_repository
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)

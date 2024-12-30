from uuid import UUID
from fastapi import APIRouter

from common.application.decorators.error_decorator import ErrorDecorator
from common.application.decorators.logger_decorator import LoggerDecorator
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.loggers.loguru_logger import LoguruLogger
from common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from inventory.application.commands.adjust.adjust_inventory_command import AdjustInventoryCommand
from inventory.application.commands.create.create_inventory_command import (
    CreateOrUpdateInventoryCommand,
)
from inventory.application.queries.find_one_product_query import (
    FindOneProductQuery,
)
from inventory.application.queries.types.dto import FindOneInventoryDto
from inventory.infrastructure.repositories.postgres.sqlalchemy.inventory_repository import (
    InventoryRepositorySqlAlchemy,
)
from inventory.infrastructure.routes.types.dto.create.create_inventory_dto import CreateInventoryDto
from inventory.infrastructure.routes.types.dto.create.adjust_inventory_dto import AdjustInventoryDto


inventory_router = APIRouter(
    prefix="/inventories",
    tags=["Inventory"],
    responses={404: {"description": "Not found"}},
)

inventory_repository = InventoryRepositorySqlAlchemy


@inventory_router.get("/{product_id}")
async def find_inventory_by_product(id: UUID):

    result = await ErrorDecorator(
        service= LoggerDecorator(
            service=FindOneProductQuery(inventory_repository=inventory_repository),
            loggers=[LoguruLogger("Find Inventory")]
        ),
        error_handler=error_response_handler,
    ).execute(data=FindOneInventoryDto(id=id.__str__()))

    return result.handle_success(handler=success_response_handler)


@inventory_router.post("/{product_id}")
async def create_or_update_inventory(product_id: str, body: CreateInventoryDto):
    
    idGenerator = UUIDGenerator()
    result = await ErrorDecorator(
        LoggerDecorator(
            service=CreateOrUpdateInventoryCommand(
                id_generator=idGenerator,
                invetory_repository=inventory_repository
            ),
            loggers=[LoguruLogger("Update inventory")]
        ), 
        error_handler=error_response_handler,
    ).execute(product_id=product_id, data=body)

    return result.handle_success(handler=success_response_handler)


@inventory_router.put("/{product_id}")
async def adjust_inventory(product_id: str, body: AdjustInventoryDto):
   
    idGenerator = UUIDGenerator()

    
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service= AdjustInventoryCommand(
                id_generator=idGenerator,
                product_repository=inventory_repository
            ),
            loggers=[LoguruLogger("Adjust inventory")]
        ),
        error_handler=error_response_handler,
    ).execute(product_id=product_id, data=body)

    return result.handle_success(handler=success_response_handler)
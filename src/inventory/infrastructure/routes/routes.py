from uuid import UUID
from fastapi import APIRouter, Depends

from common.application.decorators.error_decorator import ErrorDecorator
from common.application.decorators.logger_decorator import LoggerDecorator
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.loggers.loguru_logger import LoguruLogger
from common.infrastructure.database.database import get_session
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
from inventory.application.queries.find_inventory_query import (
    FindInventoryByProductIdQuery,
)
from inventory.application.queries.types.dto import FindOneInventoryDto
from inventory.infrastructure.repositories.postgres.sqlalchemy.inventory_repository import (
    InventoryRepositorySqlAlchemy,
)
from product.infrastructure.repositories.postgres.sqlalchemy.product_repository import (
    ProductRepositorySqlAlchemy,
)
from inventory.infrastructure.routes.types.dto.create.create_inventory_dto import CreateInventoryDto
from inventory.application.commands.types.create_inventory_dto import CreateInventoryDto as CreateInventoryDtoApp
from inventory.infrastructure.routes.types.dto.create.adjust_inventory_dto import AdjustInventoryDto
from inventory.application.commands.types.adjust_inventory_dto import AdjustInventoryDto as AdjustInventoryDtoApp


inventory_router = APIRouter(
    prefix="/inventories",
    tags=["Inventory"],
    responses={404: {"description": "Not found"}},
)



@inventory_router.get("/{product_id}")
async def find_inventory_by_product(
    id: UUID,
    session=Depends(get_session)
):
    result = await ErrorDecorator(
        service=LoggerDecorator(
            service=FindInventoryByProductIdQuery(product_repository=ProductRepositorySqlAlchemy(), inventory_repository=InventoryRepositorySqlAlchemy(session)),
            loggers=[LoguruLogger("Find Inventory")]
        ),
        error_handler=error_response_handler,
    ).execute(data=FindOneInventoryDto(id=id.__str__()))

    return result.handle_success(handler=success_response_handler)

@inventory_router.post("/{product_id}")
async def create_or_update_inventory(
    product_id: UUID, 
    body: CreateInventoryDto, 
    session=Depends(get_session)
):
    id_generator = UUIDGenerator()
    

    result = await ErrorDecorator(
        LoggerDecorator(
            service=CreateOrUpdateInventoryCommand(
                id_generator=id_generator,
                inventory_repository=InventoryRepositorySqlAlchemy(session)
            ),
            loggers=[LoguruLogger("Update inventory")]
        ), 
        error_handler=error_response_handler,
    ).execute(data=CreateInventoryDtoApp(product_id=product_id, stock=body.stock))

    return result.handle_success(handler=success_response_handler)

@inventory_router.put("/{product_id}")
async def create_or_update_inventory(
    product_id: UUID, 
    body: AdjustInventoryDto, 
    session=Depends(get_session)
):
    idGenerator = UUIDGenerator()

    
    result = await ErrorDecorator(
        service= LoggerDecorator(
            service= AdjustInventoryCommand(
                id_generator=idGenerator,
                inventory_repository=InventoryRepositorySqlAlchemy(session)
            ),
            loggers=[LoguruLogger("Adjust inventory")]
        ),
        error_handler=error_response_handler,
    ).execute(data=AdjustInventoryDtoApp(product_id=product_id, stock_change=body.stock))

    return result.handle_success(handler=success_response_handler)
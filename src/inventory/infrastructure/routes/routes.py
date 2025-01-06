from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from src.common.infrastructure.auth.models.auth_user import AuthUser, AuthUserRole
from src.common.infrastructure.auth.role_checker import role_checker
from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.application.decorators.logger_decorator import LoggerDecorator
from src.common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from src.common.infrastructure.loggers.loguru_logger import LoguruLogger
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from src.common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from src.inventory.application.commands.adjust.adjust_inventory_command import AdjustInventoryCommand
from src.inventory.application.commands.create.create_inventory_command import (
    CreateOrUpdateInventoryCommand,
)
from src.inventory.application.queries.find_inventory_query import (
    FindInventoryByProductIdQuery,
)
from src.inventory.application.queries.types.dto import FindOneInventoryDto
from src.inventory.infrastructure.repositories.postgres.sqlalchemy.inventory_repository import (
    InventoryRepositorySqlAlchemy,
)
from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import (
    ProductRepositorySqlAlchemy,
)
from src.inventory.infrastructure.routes.types.dto.create.create_inventory_dto import CreateInventoryDto
from src.inventory.application.commands.types.create_inventory_dto import CreateInventoryDto as CreateInventoryDtoApp
from src.inventory.infrastructure.routes.types.dto.create.adjust_inventory_dto import AdjustInventoryDto
from src.inventory.application.commands.types.adjust_inventory_dto import AdjustInventoryDto as AdjustInventoryDtoApp


inventory_router = APIRouter(
    prefix="/inventories",
    tags=["Inventory"],
    responses={404: {"description": "Not found"}},
)



@inventory_router.get("/{product_id}")
async def find_inventory_by_product(
    id: UUID,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    session=Depends(get_session),
):
    result = await ErrorDecorator(
        service=LoggerDecorator(
            service=FindInventoryByProductIdQuery(product_repository=ProductRepositorySqlAlchemy(session), inventory_repository=InventoryRepositorySqlAlchemy(session)),
            loggers=[LoguruLogger("Find Inventory")]
        ),
        error_handler=error_response_handler,
    ).execute(data=FindOneInventoryDto(id=id.__str__()))

    return result.handle_success(handler=success_response_handler)

@inventory_router.post("/{product_id}")
async def create_or_update_inventory(
    product_id: UUID, 
    body: CreateInventoryDto, 
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
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
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
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
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.order.application.services.create.types.dto import CreateOrderDto
from src.common.infrastructure.auth.models.auth_user import AuthUser, AuthUserRole
from src.common.infrastructure.auth.role_checker import role_checker
from src.common.infrastructure.bus.bus import get_command_bus, Bus

order_router = APIRouter(
    prefix="/orders",
    tags=["Order"],
    responses={404: {"description": "Not found"}},
)

@order_router.post("")
async def create_order_from_shopping_cart(
    user: Annotated[AuthUser, Depends(role_checker([AuthUserRole.CLIENT]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
):
    result = await command_bus.dispatch(CreateOrderDto(
        client_id=user.id,
    ))
    return result

@order_router.get("")
async def get_order_history():
    pass

@order_router.get("/{order_id}")
async def get_order(order_id: UUID):
    pass
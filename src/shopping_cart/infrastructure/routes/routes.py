from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartCommand, ItemDetail
from src.common.infrastructure.auth.db_models.auth_user_model import AuthUserRole
from src.common.infrastructure.auth.models.auth_user import AuthUser
from src.common.infrastructure.auth.role_checker import role_checker
from src.common.infrastructure.bus.bus import Bus, get_command_bus
from src.common.infrastructure.pagination.pagination_params import pagination_params
from src.shopping_cart.infrastructure.routes.types.update_cart_item_quantity import UpdateCartItemQuantity
from src.shopping_cart.infrastructure.routes.types.add_cart_items_dto import AddCartItemsDto


shopping_cart_router = APIRouter(
    prefix="/carts",
    tags=["Shopping Cart"],
    responses={404: {"description": "Not found"}},
)

@shopping_cart_router.post("/items")
async def add_item_to_cart(
    body: AddCartItemsDto,
    user: Annotated[AuthUser, Depends(role_checker([AuthUserRole.CLIENT]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
):
    result = await command_bus.dispatch(AddItemsToShoppingCartCommand(
        client_id=user.id,
        items=[
            ItemDetail(
                product_id=str(item.product_id),
                quantity=item.quantity
            ) for item in body.items]
    ))
    return result

@shopping_cart_router.put("/items/{product_id}")
def update_cart_item_quantity(
    product_id: UUID,
    body: UpdateCartItemQuantity,
):
    pass

@shopping_cart_router.delete("/items/{product_id}")
def remove_item_from_cart(
    product_id: UUID
):
    pass

@shopping_cart_router.get("")
def get_user_cart_items(
    pagination: Annotated[dict, Depends(pagination_params)]
):
    pass


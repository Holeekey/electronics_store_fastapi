from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from pymongo import MongoClient

from src.common.domain.utils.is_none import is_none
from src.common.infrastructure.database.mongo import get_mongo_client
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.shopping_cart.application.info.get_shopping_cart_info import get_shopping_cart_info
from src.shopping_cart.application.errors.not_found import shopping_cart_not_found_error
from src.shopping_cart.application.services.remove_item.types.dto import RemoveItemFromShoppingCartDto
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartDto, ItemDetail
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
    result = await command_bus.dispatch(AddItemsToShoppingCartDto(
        client_id=user.id,
        items=[
            ItemDetail(
                product_id=str(item.product_id),
                quantity=item.quantity
            ) for item in body.items]
    ))
    return result

@shopping_cart_router.put("/items/{product_id}")
async def update_cart_item_quantity(
    product_id: UUID,
    body: UpdateCartItemQuantity,
    user: Annotated[AuthUser, Depends(role_checker([AuthUserRole.CLIENT]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
):
    result = await command_bus.dispatch(AddItemsToShoppingCartDto(
        client_id=user.id,
        items=[
            ItemDetail(
                product_id=str(product_id),
                quantity=body.quantity
            )
        ]
    ))
    return result

@shopping_cart_router.delete("/items/{product_id}")
async def remove_item_from_cart(
    product_id: UUID,
    user: Annotated[AuthUser, Depends(role_checker([AuthUserRole.CLIENT]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
):
    result = await command_bus.dispatch(RemoveItemFromShoppingCartDto(
        client_id=user.id,
        product_id=str(product_id)
    ))
    return result
    

@shopping_cart_router.get("")
def get_user_cart_items(
    user: Annotated[AuthUser, Depends(role_checker([AuthUserRole.CLIENT]))],
    session: Annotated[MongoClient,Depends(get_mongo_client)]
):
    db = session["template"]
    user_coll = db["shopping_cart"]
    
    projection = {
        "_id": 0,
        "user_id": 0
    }
    
    cart = user_coll.find_one({"user_id": user.id},projection)
    
    if is_none(cart):
        error = shopping_cart_not_found_error()
        raise error_response_handler(error)
    
    return success_response_handler(
        cart,
        get_shopping_cart_info()
    )


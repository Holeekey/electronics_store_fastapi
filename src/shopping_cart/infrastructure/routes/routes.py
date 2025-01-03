from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from src.common.infrastructure.pagination.pagination_params import pagination_params
from src.shopping_cart.infrastructure.routes.types.update_cart_item_quantity import UpdateCartItemQuantity
from src.shopping_cart.infrastructure.routes.types.add_cart_items_dto import AddCartItemsDto


shopping_cart_router = APIRouter(
    prefix="/carts",
    tags=["Shopping Cart"],
    responses={404: {"description": "Not found"}},
)

@shopping_cart_router.post("/items")
def add_item_to_cart(
    body: AddCartItemsDto
):
    pass

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


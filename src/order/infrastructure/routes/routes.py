from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pymongo import MongoClient

from src.order.application.services.set_status.types.dto import SetOrderStatusDto as SetOrderStatusDtoApp
from src.order.infrastructure.routes.types.set_order_status_dto import SetOrderStatusDto
from src.common.domain.utils.is_none import is_none
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.infrastructure.pagination.utils.pagination_to_skip import pagination_to_skip
from src.common.infrastructure.responses.handlers.pagination_response_handler import pagination_response_handler
from src.common.infrastructure.responses.pagination_response import PaginationInfo
from src.order.application.info.get_order_history_info import get_order_history_info
from src.order.application.info.get_order_detail_info import get_order_detail_info
from src.order.application.errors.not_found import order_not_found_error
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.common.infrastructure.pagination.pagination_params import pagination_params
from src.common.infrastructure.database.mongo import get_mongo_client
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

@order_router.patch("")
async def set_order_status(
    order_id: UUID,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    command_bus: Annotated[Bus, Depends(get_command_bus)],
    body: SetOrderStatusDto
):
    result = await command_bus.dispatch(SetOrderStatusDtoApp(
        order_id=str(order_id),
        status=body.status,
    ))
    return result

@order_router.get("")
async def get_order_history(
    user: Annotated[AuthUser, Depends(role_checker([AuthUserRole.CLIENT]))],
    session: Annotated[MongoClient,Depends(get_mongo_client)],
    pagination: Annotated[dict, Depends(pagination_params)],
):
    db = session["template"]
    order_coll = db["order"]
    
    projection = {
        "_id": 0,
        "user_id": 0,
        "items": 0,
    }
    
    where = { "user_id": user.id }
    
    orders_cursor = order_coll.find(where, projection).sort("creation_date", -1).skip(pagination_to_skip(pagination)).limit(pagination["per_page"])
    total_count = order_coll.count_documents(where)
    orders = list(orders_cursor)
    pagination_info = PaginationInfo.make_pagination_info(pagination["page"], pagination["per_page"], total_count)
    
    return pagination_response_handler(
        t=orders,
        info=get_order_history_info(),
        pagination_info=pagination_info
    )

@order_router.get("/{order_id}")
async def get_order_detail(
    order_id: UUID,
    user: Annotated[AuthUser, Depends(role_checker([AuthUserRole.CLIENT]))],
    session: Annotated[MongoClient,Depends(get_mongo_client)],
    pagination: Annotated[dict, Depends(pagination_params)],
):
    db = session["template"]
    order_coll = db["order"]
    
    projection = {
        "_id": 0,
        "user_id": 0,
    }
    
    where = {"user_id": user.id, "order_id": str(order_id)}
    
    order = order_coll.find_one(where, projection)
    
    if is_none(order):
        error = order_not_found_error()
        raise error_response_handler(error)
    
    total_count = len(order["items"])
    pagination_info = PaginationInfo.make_pagination_info(pagination["page"], pagination["per_page"], total_count)
    
    start = pagination_to_skip(pagination)
    end = start + pagination["per_page"]
    
    return pagination_response_handler(
        t={
            "order_id": order["order_id"],
            "total_price": order["total_price"],
            "status": order["status"],
            "creation_date": order["creation_date"],
            "items": order["items"][start:end],    
        },
        info=get_order_detail_info(),
        pagination_info=pagination_info
    )
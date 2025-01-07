from typing import Annotated
from pydantic import UUID4
from fastapi import APIRouter, HTTPException, status, Depends
from pymongo import MongoClient

from src.common.infrastructure.auth.models.auth_user import AuthUser, AuthUserRole
from src.common.infrastructure.auth.role_checker import role_checker
from src.common.infrastructure.bus.bus import Bus, get_command_bus
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.database.mongo import get_mongo_client
from src.common.infrastructure.responses.pagination_response import PaginationInfo
from src.common.infrastructure.pagination.pagination_params import pagination_params
from src.common.infrastructure.pagination.utils.pagination_to_skip import pagination_to_skip
from src.common.infrastructure.responses.handlers.pagination_response_handler import pagination_response_handler
from src.common.domain.utils.is_none import is_none

from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.infrastructure.database.database import SessionLocal
from src.common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from src.common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from src.common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from src.product.application.commands.create.create_product_command import (
    CreateProductCommand,
)
from src.product.application.commands.update.types.dto import UpdateProductDto
from src.product.application.commands.update.update_product_command import (
    UpdateProductCommand,
)
from src.product.application.commands.delete.types.dto import DeleteProductDto
from src.product.application.commands.delete.delete_product_command import (
    DeleteProductCommand,
)
from src.product.application.queries.find_one.find_one_product_query import (
    FindOneProductQuery,
)
from src.product.application.queries.find_one.types.dto import FindOneProductDto
from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import (
    ProductRepositorySqlAlchemy,
)
from src.product.infrastructure.routes.types.create_product_dto import CreateProductDto
from src.product.infrastructure.routes.types.update_product_dto import UpdateProductQueryDto
from src.product.domain.value_objects.product_status import ProductStatusOptions
from src.product.application.errors.not_found import product_not_found_error
from src.product.application.info.product_found_info import product_found_info
from src.product.application.info.product_found_many_info import product_found_many_info

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    responses={404: {"description": "Not found"}},
)

product_repository = ProductRepositorySqlAlchemy(SessionLocal())

@product_router.post("")
async def create_product(
        body: CreateProductDto,
        _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN, AuthUserRole.MANAGER]))],
        command_bus: Annotated[Bus, Depends(get_command_bus)]
    ):

    result = await command_bus.dispatch(body)
    return result

@product_router.put("/{id}")
async def update_product(
        id:UUID4, 
        body: UpdateProductQueryDto,
        _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN, AuthUserRole.MANAGER]))],
        command_bus: Annotated[Bus, Depends(get_command_bus)]
    ):

    service_dto = UpdateProductDto(id=str(id), code=body.code, name=body.name, description=body.description, cost=body.cost, margin=body.margin)
    result = await command_bus.dispatch(service_dto)
    return result

@product_router.delete("/{id}")
async def delete_product(
        id:UUID4,
        _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN, AuthUserRole.MANAGER]))],
        command_bus: Annotated[Bus, Depends(get_command_bus)]
    ):

    service_dto = DeleteProductDto(id=str(id))
    result = await command_bus.dispatch(service_dto)
    return result

@product_router.get("/one/{id}")
async def find_one_product(
        id: UUID4,
        _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN, AuthUserRole.MANAGER, AuthUserRole.CLIENT]))],
        session: Annotated[MongoClient, Depends(get_mongo_client)]
    ):

    db = session["template"]
    product_coll = db["product"]

    projection = {
        "_id": 0,
    }

    product = product_coll.find_one({"id": str(id), "status":ProductStatusOptions.ACTIVE.value}, projection)
    if is_none(product):
        error = product_not_found_error()
        raise error_response_handler(error)

    return success_response_handler(
        product,
        product_found_info()
    )

@product_router.get("/many")
async def find_many_products(
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN, AuthUserRole.MANAGER, AuthUserRole.CLIENT]))],
    session: Annotated[MongoClient, Depends(get_mongo_client)],
    pagination: Annotated[dict, Depends(pagination_params)]
    ):
    
    db = session["template"]
    product_coll = db["product"]

    projection = {
        "_id": 0,
    }

    where = {"status": ProductStatusOptions.ACTIVE.value}
    products_cursor = product_coll.find(where, projection).skip(pagination_to_skip(pagination)).limit(pagination["per_page"])
    total_count = product_coll.count_documents(where)
    products = list(products_cursor)
    pagination_info = PaginationInfo.make_pagination_info(pagination["page"], pagination["per_page"], total_count)

    return pagination_response_handler(t=products, info=product_found_many_info(), pagination_info=pagination_info)
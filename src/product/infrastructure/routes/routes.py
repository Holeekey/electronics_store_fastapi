from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from common.application.decorators.error_decorator import ErrorDecorator
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.responses.handlers.error_response_handler import (
    error_response_handler,
)
from common.infrastructure.responses.handlers.success_response_handler import (
    success_response_handler,
)
from product.application.commands.create.create_product_command import (
    CreateProductCommand,
)
from product.application.commands.update.types.dto import UpdateProductDto
from product.application.commands.update.update_product_command import (
    UpdateProductCommand,
)
from product.application.commands.delete.types.dto import DeleteProductDto
from product.application.commands.delete.delete_product_command import (
    DeleteProductCommand,
)
from product.application.queries.find_one.find_one_product_query import (
    FindOneProductQuery,
)
from product.application.queries.find_one.types.dto import FindOneProductDto
from product.infrastructure.repositories.postgres.sqlalchemy.product_repository import (
    ProductRepositorySqlAlchemy,
)
from product.infrastructure.routes.types.create_product_dto import CreateProductDto
from product.infrastructure.routes.types.update_product_dto import UpdateProductQueryDto

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    responses={404: {"description": "Not found"}},
)

product_repository = ProductRepositorySqlAlchemy()


@product_router.get("/one/{id}")
async def find_one_product(id: UUID):

    result = await ErrorDecorator(
        service=FindOneProductQuery(product_repository=product_repository),
        error_handler=error_response_handler,
    ).execute(data=FindOneProductDto(id=id.__str__()))

    return result.handle_success(handler=success_response_handler)

@product_router.get("/many")
async def find_many_products(page:int = 1, per_page:int = 5): #to-do This should be implemented via CQRS
    
    if (page < 1) or (per_page < 1):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Page indexes start at 1. Must show at least one entry per page")
    result = product_repository.find_many(page, per_page)
    if (result is None):
        raise HTTPException(status_code=404, detail="No products found")

    return result

@product_router.post("")
async def create_product(body: CreateProductDto):

    # idGenerator = RandomIdGenerator()
    idGenerator = UUIDGenerator()

    result = await ErrorDecorator(
        service=CreateProductCommand(
            id_generator=idGenerator, product_repository=product_repository
        ),
        error_handler=error_response_handler,
    ).execute(data=body)

    return result.handle_success(handler=success_response_handler)

@product_router.put("{id}")
async def update_product(id:UUID, body: UpdateProductQueryDto):

    service_dto = UpdateProductDto(id=str(id), code=body.code, name=body.name, description=body.description, cost=body.cost, margin=body.margin)
    result = await ErrorDecorator(
        service=UpdateProductCommand(
            product_repository=product_repository
        ),
        error_handler=error_response_handler
    ).execute(data=service_dto)

    return result.handle_success(handler=success_response_handler)

@product_router.delete("{id}")
async def delete_product(id:UUID):

    service_dto = DeleteProductDto(id=str(id))
    result = await ErrorDecorator(
        service=DeleteProductCommand(
            product_repository=product_repository
        ),
        error_handler=error_response_handler
    ).execute(data=service_dto)

    return result.handle_success(handler=success_response_handler)

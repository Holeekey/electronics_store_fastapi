from uuid import UUID
from fastapi import APIRouter

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
from product.application.queries.find_one.find_one_product_query import (
    FindOneProductQuery,
)
from product.application.queries.find_one.types.dto import FindOneProductDto
from product.infrastructure.repositories.postgres.sqlalchemy.product_repository import (
    ProductRepositorySqlAlchemy,
)
from product.infrastructure.routes.types.create_product_dto import CreateProductDto


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
    ).execute(data=FindOneProductDto(id=id))

    return result.handle_success(handler=success_response_handler)


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

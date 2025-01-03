from src.common.application.id_generator.id_generator import IDGenerator
from src.common.application.service.application_service import IApplicationService

from src.common.domain.result.result import Result
from src.common.domain.utils.is_not_none import is_not_none
from src.product.application.commands.create.types.dto import CreateProductDto
from src.product.application.commands.create.types.response import CreateProductResponse
from src.product.application.info.product_created_info import product_created_info
from src.product.application.repositories.product_repository import IProductRepository
from src.product.domain.factories.product_factory import product_factory
from src.product.domain.value_objects.product_name import ProductName

from src.product.application.errors.name_already_exists import (
    product_name_already_exists_error,
)


class CreateProductCommand(IApplicationService):

    def __init__(
        self, id_generator: IDGenerator, product_repository: IProductRepository
    ):
        self.id_generator = id_generator
        self.product_repository = product_repository

    async def execute(self, data: CreateProductDto) -> Result[CreateProductResponse]:

        product_by_name = await self.product_repository.find_by_name(
            name=ProductName(data.name)
        )

        if is_not_none(product_by_name):
            return Result.failure(error=product_name_already_exists_error())

        id = self.id_generator.generate()

        product = product_factory(id=id, code=data.code, name=data.name, description=data.description, cost=data.cost, margin=data.margin, status=1) #Products start created as 'ACTIVE'

        await self.product_repository.save(product=product)

        return Result.success(
            value=CreateProductResponse(id=product.id), info=product_created_info()
        )

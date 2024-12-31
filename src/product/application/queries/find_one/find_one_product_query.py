from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result
from src.product.application.info.product_found_info import product_found_info
from src.product.application.queries.find_one.types.dto import FindOneProductDto
from src.product.application.queries.find_one.types.response import FindOneProductResponse
from src.product.application.repositories.product_repository import IProductRepository
from src.product.domain.value_objects.product_id import ProductId
from src.common.domain.utils.is_none import is_none
from src.product.application.errors.not_found import product_not_found_error


class FindOneProductQuery(IApplicationService):
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    async def execute(self, data: FindOneProductDto) -> Result[FindOneProductResponse]:

        product = await self.product_repository.find_one(id=ProductId(data.id))

        if is_none(product):
            return Result.failure(product_not_found_error())

        return Result.success(
            FindOneProductResponse(
                id=product.id.id, name=product.name.name, price=product.pricing.price
            ),
            product_found_info(),
        )

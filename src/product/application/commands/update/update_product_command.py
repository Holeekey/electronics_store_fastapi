from common.domain.result.result import Result, result_info_factory
from common.application.service.application_service import IApplicationService

from common.domain.utils.is_none import is_none
from product.application.commands.update.types.dto import UpdateProductDto
from product.application.commands.update.types.response import UpdateProductResponse
from product.application.repositories.product_repository import IProductRepository
from product.domain.value_objects.product_id import ProductId
from product.domain.factories.product_factory import product_factory

from product.application.errors.not_found import product_not_found_error

class UpdateProductCommand(IApplicationService):

    def __init__(self, product_repository:IProductRepository):
        self.product_repository = product_repository

    async def execute(self, data: UpdateProductDto) -> UpdateProductResponse:
        old_product = await self.product_repository.find_one(ProductId(data.id))
        if is_none(old_product):
            return Result.failure(error=product_not_found_error())
        if (old_product.status.status == 0):
            return Result.failure(error=product_not_found_error())
        
        new_product = product_factory(id=data.id, code=data.code, name=data.name, description=data.description, cost=data.cost, margin=data.margin, status=old_product.status.status)
        update_result = await self.product_repository.update(new_product)

        if (update_result.is_error()):
            return Result.failure(error=update_result.handle_error(handler=(lambda x: x)))
        new_product = update_result.unwrap()
        response = UpdateProductResponse(id=new_product.id.id, code=new_product.code.code, name=new_product.name.name, description=new_product.description.description, cost=new_product.pricing.cost, margin=new_product.pricing.margin, price=new_product.pricing.price)
        return Result.success(value=response)
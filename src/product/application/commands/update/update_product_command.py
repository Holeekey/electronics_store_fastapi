from src.common.domain.result.result import Result, result_info_factory
from src.common.application.service.application_service import IApplicationService

from src.common.domain.utils.is_none import is_none
from src.product.application.commands.update.types.dto import UpdateProductDto
from src.product.application.commands.update.types.response import UpdateProductResponse
from src.product.application.repositories.product_repository import IProductRepository
from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.factories.product_factory import product_factory

from src.product.application.errors.not_found import product_not_found_error

class UpdateProductCommand(IApplicationService):

    def __init__(self, product_repository:IProductRepository):
        self.product_repository = product_repository

    async def execute(self, data: UpdateProductDto) -> Result[UpdateProductResponse]:
        old_product = await self.product_repository.find_one(ProductId(data.id))
        if is_none(old_product):
            return Result.failure(error=product_not_found_error())
        if (old_product.status.status.value == 0):
            return Result.failure(error=product_not_found_error()) #? De lo que revisé del repositorio, este caso no se va a dar nunca
        
        new_product = product_factory(id=data.id, code=data.code, name=data.name, description=data.description, cost=data.cost, margin=data.margin, status=old_product.status.status.value)
        update_result = await self.product_repository.update(id=old_product.id, new_product=new_product)

        if (update_result.is_error()):
            return Result.failure(error=update_result.handle_error(handler=(lambda x: x)))
        new_product = update_result.unwrap()
        response = UpdateProductResponse(id=new_product.id.id, code=new_product.code.code, name=new_product.name.name, description=new_product.description.description, cost=new_product.pricing.cost, margin=new_product.pricing.margin, price=new_product.pricing.price)
        info = result_info_factory("UPD-001", "Product updated successfully")
        return Result.success(value=response, info=info())
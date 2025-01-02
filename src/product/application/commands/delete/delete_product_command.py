from src.common.domain.result.result import Result, result_info_factory
from src.common.application.service.application_service import IApplicationService

from src.common.domain.utils.is_none import is_none
from src.product.application.commands.delete.types.dto import DeleteProductDto
from src.product.application.commands.delete.types.response import DeleteProductResponse
from src.product.application.repositories.product_repository import IProductRepository
from src.product.domain.value_objects.product_id import ProductId

from src.product.application.errors.not_found import product_not_found_error

class DeleteProductCommand(IApplicationService):

    def __init__(self, product_repository:IProductRepository):
        self.product_repository = product_repository

    async def execute(self, data: DeleteProductDto) -> DeleteProductResponse:
        target_product = await self.product_repository.find_one(ProductId(data.id))
        if is_none(target_product):
            return Result.failure(error=product_not_found_error())
        if (target_product.status.status.value == 0):
            return Result.failure(error=product_not_found_error())
        
        delete_result = await self.product_repository.delete(target_product)

        if (delete_result.is_error()):
            return Result.failure(error=delete_result.handle_error(handler=(lambda x: x)))
        response = DeleteProductResponse(id=target_product.id.id)
        info = result_info_factory("DEL-001", "Product deactivated successfully")
        return Result.success(value=response, info=info())
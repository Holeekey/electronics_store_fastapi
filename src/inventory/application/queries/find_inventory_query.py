from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result
from src.common.domain.utils.is_not_none import is_not_none
from src.inventory.application.queries.types.response import FindOneInventoryResponse
from src.inventory.application.repositories.inventory_repository import IInventoryRepository
from src.product.application.info.product_found_info import product_found_info
from src.product.application.queries.find_one.types.dto import FindOneProductDto
from src.product.application.repositories.product_repository import IProductRepository
from src.product.domain.value_objects.product_id import ProductId
from src.common.domain.utils.is_none import is_none
from src.product.application.errors.not_found import product_not_found_error


class FindInventoryByProductIdQuery(IApplicationService):
    def __init__(self, product_repository: IProductRepository, inventory_repository: IInventoryRepository):
        self.product_repository = product_repository
        self.inventory_repository = inventory_repository

    async def execute(self, data: FindOneProductDto) -> Result[FindOneInventoryResponse]:

        product = await self.product_repository.find_one(id=ProductId(data.id))

        if is_none(product):
            return Result.failure(product_not_found_error())

        inventory = await self.inventory_repository.find_by_product_id(ProductId(data.id))

        stock = inventory.stock.value if is_not_none(inventory) else 0

        return Result.success(
            FindOneInventoryResponse(
                product_name=product.name.name,
                product_id=product.id.id,
                stock=stock
            ),
            product_found_info(),
        )

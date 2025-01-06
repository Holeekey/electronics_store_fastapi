from src.common.domain.result.result import Result, result_info_factory
from src.common.application.service.application_service import IApplicationService
from src.common.application.events.event_handlers import IEventPublisher

from src.common.domain.utils.is_none import is_none
from src.product.application.commands.delete.types.dto import DeleteProductDto
from src.product.application.commands.delete.types.response import DeleteProductResponse
from src.product.application.repositories.product_repository import IProductRepository
from src.product.domain.value_objects.product_id import ProductId

from src.common.domain.error.domain_error import DomainError
from src.product.application.errors.not_found import product_not_found_error
from src.product.application.info.product_deleted_info import product_deleted_info

class DeleteProductCommand(IApplicationService):

    def __init__(self, product_repository:IProductRepository, publisher: IEventPublisher):
        self.product_repository = product_repository
        self.event_publisher = publisher

    async def execute(self, data: DeleteProductDto) -> Result[DeleteProductResponse]:
        target_product = await self.product_repository.find_one(ProductId(data.id))
        if is_none(target_product):
            return Result.failure(error=product_not_found_error())
        target_product.pull_events() #Discard 'product_created' event, since it is of no interest here
        if (target_product.status.status.value == 0):
            return Result.failure(error=product_not_found_error()) #? De lo que revisé del repositorio, este caso no se va a dar nunca
        
        try:
            target_product.delete()
        except DomainError as error:
            return Result.failure(error=error)
        
        delete_result = await self.product_repository.delete(target_product)
        if (delete_result.is_error()):
            return Result.failure(error=delete_result.handle_error(handler=(lambda x: x)))
        response = DeleteProductResponse(id=target_product.id.id)
        
        # Since process was successful, publish related event
        await self.event_publisher.publish(target_product.pull_events())
        return Result.success(value=response, info=product_deleted_info())
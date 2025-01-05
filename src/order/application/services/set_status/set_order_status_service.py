
from dataclasses import dataclass
from uuid import UUID
from src.order.application.info.set_order_status_info import set_order_status_info
from src.common.application.events.event_handlers import IEventPublisher
from src.common.domain.result.result import Result
from src.common.domain.utils.is_none import is_none
from src.order.application.errors.not_found import order_not_found_error
from src.order.application.errors.not_cancelable import order_not_cancelable_error
from src.order.application.errors.not_completable import order_not_completable_error
from src.order.application.repositories.order_repository import IOrderRepository
from src.order.application.services.set_status.types.dto import OrderStatusOptionsDto, SetOrderStatusDto
from src.order.application.services.set_status.types.response import SetOrderStatusResponse
from src.order.domain.value_objects.order_id import OrderId
from src.common.application.service.application_service import IApplicationService

@dataclass
class SetOrderStatusService(IApplicationService):
    
    order_repository: IOrderRepository
    event_publisher: IEventPublisher
    
    async def execute(self, data: SetOrderStatusDto) -> Result[SetOrderStatusResponse]:
        
        order = await self.order_repository.find_one(OrderId(UUID(data.order_id)))
        
        if is_none(order):
            return Result.failure(order_not_found_error())
        
        order.clear_events()
        
        if data.status.name == OrderStatusOptionsDto.COMPLETED.name:
            
            if not order.status.is_completable():
                return Result.failure(order_not_completable_error())
            
            order.complete()   
            
        else:
            
            if not order.status.is_cancelable():
                return Result.failure(order_not_cancelable_error())
                
            order.cancel()
                
        await self.order_repository.save(order)
        
        await self.event_publisher.publish(order.pull_events())
        
        return Result.success(SetOrderStatusResponse("Succesful"), set_order_status_info())
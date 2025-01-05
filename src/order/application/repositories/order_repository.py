
from abc import ABCMeta, abstractmethod
from typing import Optional

from src.order.domain.value_objects.order_id import OrderId
from src.order.domain.order import Order


class IOrderRepository(metaclass=ABCMeta):
    
    @abstractmethod
    async def find_one(self, order_id: OrderId) -> Optional[Order]:
        pass
    
    @abstractmethod
    async def save(self, order: Order) -> None:
        pass

from abc import ABCMeta, abstractmethod

from src.order.domain.order import Order


class IOrderRepository(metaclass=ABCMeta):
    
    @abstractmethod
    async def save(self, order: Order) -> None:
        pass

from dataclasses import dataclass
from enum import Enum

class OrderStatusOptionsDto(Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class SetOrderStatusDto:
    order_id: str
    status: OrderStatusOptionsDto
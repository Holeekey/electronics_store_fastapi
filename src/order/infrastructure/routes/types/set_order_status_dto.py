from enum import Enum
from pydantic import BaseModel

from src.order.application.services.set_status.types.dto import OrderStatusOptionsDto

class SetOrderStatusDto(BaseModel):
    status: OrderStatusOptionsDto

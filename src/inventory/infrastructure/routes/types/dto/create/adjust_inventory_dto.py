from uuid import UUID
from pydantic import BaseModel


class AdjustInventoryDto(BaseModel):
    product_id: UUID
    stock: int
    
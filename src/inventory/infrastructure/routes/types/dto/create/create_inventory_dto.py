from uuid import UUID
from pydantic import BaseModel


class CreateInventoryDto(BaseModel):
    product_id: UUID
    stock: int
    
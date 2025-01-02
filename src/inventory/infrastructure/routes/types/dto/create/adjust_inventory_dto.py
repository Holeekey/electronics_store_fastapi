from uuid import UUID
from pydantic import BaseModel


class AdjustInventoryDto(BaseModel):
    stock: int
    
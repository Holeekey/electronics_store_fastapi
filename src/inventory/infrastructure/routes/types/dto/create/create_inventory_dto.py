from uuid import UUID
from pydantic import BaseModel


class CreateInventoryDto(BaseModel):
    stock: int
    
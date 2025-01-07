from pydantic import BaseModel, Field


class CreateInventoryDto(BaseModel):
    stock: int = Field(min = 0)
    
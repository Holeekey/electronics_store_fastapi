from pydantic import BaseModel, Field


class AdjustInventoryDto(BaseModel):
    stock: int = Field(min = 0)
    
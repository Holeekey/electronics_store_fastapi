from pydantic import BaseModel


class AdjustInventoryDto(BaseModel):
    product_id: str
    stock: int
    
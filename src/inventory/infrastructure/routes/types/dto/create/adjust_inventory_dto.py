from pydantic import BaseModel


class adjustInventoryDto(BaseModel):
    product_id: str
    stock: int
    
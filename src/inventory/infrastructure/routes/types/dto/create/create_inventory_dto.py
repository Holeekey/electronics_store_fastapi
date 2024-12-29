from pydantic import BaseModel


class CreateInventoryDto(BaseModel):
    product_id: str
    stock: int
    
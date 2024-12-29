from pydantic import BaseModel


class CreateInventoryDto(BaseModel):
    product_id: int
    stock: int
    
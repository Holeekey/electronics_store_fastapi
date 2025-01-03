from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

class CartItemDetail(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)

class AddCartItemsDto(BaseModel):
    items: List[CartItemDetail]
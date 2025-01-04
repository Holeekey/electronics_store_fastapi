from pydantic import BaseModel, Field


class UpdateCartItemQuantity(BaseModel):
    quantity: int = Field(gt=0)
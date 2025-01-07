from pydantic import BaseModel, Field


class CreateProductDto(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=3)
    description: str
    cost: float = Field(gt=0)
    margin: float = Field(gt=0,lt=1)

from pydantic import BaseModel


class CreateProductDto(BaseModel):
    code: str
    name: str
    description: str
    cost: float
    margin: float

from pydantic import BaseModel


class UpdateProductQueryDto(BaseModel):
    code: str
    name: str
    description: str
    cost: float
    margin: float

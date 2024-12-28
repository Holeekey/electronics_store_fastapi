from pydantic import BaseModel


class CreateUserDto(BaseModel):
    product_id: int
    stock: int
    
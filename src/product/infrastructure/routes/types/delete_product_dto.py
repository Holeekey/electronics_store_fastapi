from pydantic import BaseModel

class DeleteProductDto(BaseModel):
    id: str
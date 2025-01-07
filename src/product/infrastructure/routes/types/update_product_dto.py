from typing import Optional
from pydantic import BaseModel, Field


class UpdateProductQueryDto(BaseModel):
    code: Optional[str] = Field(min_length=1, default=None)
    name: Optional[str] = Field(min_length=3, default=None)
    description: Optional[str] = Field(default=None)
    cost: Optional[float] = Field(gt=0, default=None)
    margin: Optional[float] = Field(gt=0,lt=1, default=None)

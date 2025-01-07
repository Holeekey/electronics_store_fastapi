from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"
    MANAGER = "manager"


class CreateUserDto(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr = Field()
    role: UserRole

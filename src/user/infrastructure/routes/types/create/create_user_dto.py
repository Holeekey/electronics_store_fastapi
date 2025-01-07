from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"
    MANAGER = "manager"


class CreateUserDto(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr | None = Field(default=None)
    role: UserRole

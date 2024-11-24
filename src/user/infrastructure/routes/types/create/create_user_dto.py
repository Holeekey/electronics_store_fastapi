from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"
    MANAGER = "manager"


class CreateUserDto(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    role: UserRole

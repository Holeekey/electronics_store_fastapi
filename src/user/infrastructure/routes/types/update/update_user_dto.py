from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.user.infrastructure.routes.types.create.create_user_dto import UserRole

class UserStatus(str, Enum):
  ACTIVE = "active"
  SUSPENDED = "suspended"

class UpdateUserDto(BaseModel):
  id: str
  username: Optional[str] = Field(min_length=3, default=None)
  email: Optional[EmailStr] = Field(default=None)
  password: Optional[str] = Field(min_length=6, default=None)
  first_name: Optional[str] = Field(min_length=1, default=None)
  last_name: Optional[str] = Field(min_length=1, default=None)
  status: Optional[UserStatus] = Field(default=None)
      
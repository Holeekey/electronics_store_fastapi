from enum import Enum
from typing import Optional

from pydantic import BaseModel

from user.infrastructure.routes.types.create.create_user_dto import UserRole

class UserStatus(str, Enum):
  ACTIVE = "active"
  SUSPENDED = "suspended"

class UpdateUserDto(BaseModel):
  id: str
  username: Optional[str] = None
  email: Optional[str] = None
  password: Optional[str] = None
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  role: Optional[UserRole] = None
  status: Optional[UserStatus] = None
      
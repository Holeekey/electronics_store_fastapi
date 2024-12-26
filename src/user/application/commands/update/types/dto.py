from typing import Optional

from user.application.models.user import UserRole, UserStatus

class UpdateUserDto:
  def __init__(
      self, 
      id: str, 
      username: Optional[str],
      email: Optional[str],
      password: Optional[str],
      first_name: Optional[str],
      last_name: Optional[str],
      current_role: UserRole,
      new_role: Optional[UserRole],
      status: Optional[UserStatus]
      ):
    self.id = id
    self.username = username
    self.email = email
    self.password = password
    self.first_name = first_name
    self.last_name = last_name
    self.current_role = current_role
    self.new_role = new_role
    self.status = status
    
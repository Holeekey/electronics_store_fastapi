from typing import Optional

from src.user.application.models.user import UserRole, UserStatus

class UpdateUserDto:
  def __init__(
      self, 
      id: str, 
      username: Optional[str] = None,
      email: Optional[str] = None,
      password: Optional[str] = None,
      first_name: Optional[str] = None,
      last_name: Optional[str]= None,
      status: Optional[UserStatus] = None,
      role_to_update: Optional[UserRole] = None
      ):
    self.id = id
    self.username = username
    self.email = email
    self.password = password
    self.first_name = first_name
    self.last_name = last_name
    self.status = status
    self.role_to_update = role_to_update
    
  def to_dict(self):
      return (
          f"UpdateUserDto(id={self.id}, "
          f"username={self.username}, "
          f"email={self.email}, "
          f"first_name={self.first_name}, "
          f"last_name={self.last_name}, "
          f"status={self.status}, "
          f"role_to_update={self.role_to_update})"
      )
    
from user.application.models.user import UserRole, UserStatus


class FindAllManagersResponse:
  def __init__(
      self,
      id: str,
      username: str,
      email: str,
      first_name: str,
      last_name: str,
      role: UserRole,
      status: UserStatus,
      ):
    self.id = id
    self.username = username
    self.email = email
    self.first_name = first_name
    self.last_name = last_name
    self.role = role
    self.status = status
    
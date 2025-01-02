from src.user.application.models.user import UserRole, UserStatus


class FindOneUserResponse:
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        email: str,
        role: UserRole,
        status: UserStatus,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.status = status

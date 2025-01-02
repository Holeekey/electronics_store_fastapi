from src.user.application.models.user import UserRole


class CreateUserDto:
    def __init__(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        email: str,
        user_role: UserRole,
    ):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = user_role

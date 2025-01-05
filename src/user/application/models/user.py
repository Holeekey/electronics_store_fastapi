from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    CLIENT = "client"
    MANAGER = "manager"


class UserStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class User:
    def __init__(
        self,
        id: str,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        role: UserRole,
        status: UserStatus,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.username = username
        self.role = role
        self.status = status

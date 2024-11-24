
from enum import Enum


class AuthUserRole(Enum):
    ADMIN = 'admin'
    CLIENT = 'client'
    MANAGER = 'manager'

class AuthUserStatus(Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'

class AuthUser:
    def __init__(self, id: int, username: str, email: str, role: AuthUserRole, status: AuthUserStatus):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.status = status
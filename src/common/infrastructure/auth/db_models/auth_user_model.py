from enum import Enum
from sqlalchemy import Column, String, Enum as SqlEnum
from common.infrastructure.database.database import Base


class AuthUserStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class AuthUserRole(Enum):
    ADMIN = "admin"
    CLIENT = "client"
    MANAGER = "manager"


# IMPORTANTE: Tener en sincronía con el modelo del módulo de Usuario

class AuthUserModel(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(SqlEnum(AuthUserRole))
    status = Column(SqlEnum(AuthUserStatus))

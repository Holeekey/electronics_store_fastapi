from sqlalchemy import or_
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from common.infrastructure.database.database import SessionLocal
from user.application.info import user_created_info
from user.application.models.user import User
from user.application.repositories.user_repository import IUserRepository
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel, UserRole
from sqlalchemy.orm import Session


class UserRepositorySqlAlchemy(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def map_model_to_user(self, user_orm: UserModel) -> User:
        return User(
            id=user_orm.id,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            role=user_orm.role,
            status=user_orm.status,
        )

    async def find_one(self, id: str):
        user_orm = self.db.query(UserModel).filter(UserModel.id == id).first()
        if is_none(user_orm):
            return None
        return self.map_model_to_user(user_orm)

    async def find_by_username(self, username: str):
        user_orm = (
            self.db.query(UserModel).filter(UserModel.username == username).first()
        )
        if is_none(user_orm):
            return None
        return self.map_model_to_user(user_orm)

    async def find_by_email(self, email: str):
        user_orm = self.db.query(UserModel).filter(UserModel.email == email).first()
        if is_none(user_orm):
            return None
        return self.map_model_to_user(user_orm)

    async def find_by_login_credential(self, login_credential: str):

        user_orm = (
            self.db.query(UserModel)
            .filter(
                or_(
                    UserModel.username == login_credential,
                    UserModel.email == login_credential,
                )
            )
            .first()
        )
        if is_none(user_orm):
            return None

        return self.map_model_to_user(user_orm)

    async def find_by_role(self, role: UserRole):
        users_orm = self.db.query(UserModel).filter(UserModel.role == role.name).all()

        return [self.map_model_to_user(user_orm) for user_orm in users_orm]


    async def find_all(self):
        users_orm = self.db.query(UserModel).all()
        return [self.map_model_to_user(user_orm) for user_orm in users_orm]

    async def save(self, user: User) -> Result[User]:
        user_orm = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.name,
            status=user.status.name,
        )
        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return Result.success(user, info=user_created_info)

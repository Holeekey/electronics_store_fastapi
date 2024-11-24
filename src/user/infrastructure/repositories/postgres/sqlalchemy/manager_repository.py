from common.domain.utils.is_none import is_none
from user.application.models.user import UserRole
from user.application.repositories.manager_repository import IManagerRepository
from sqlalchemy.orm import Session
from common.infrastructure.database.database import SessionLocal
from user.domain.manager.factories.manager_factory import manager_factory
from user.domain.manager.value_objects.manager_id import ManagerId
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel


class ManagerRepositorySqlAlchemy(IManagerRepository):
    def __init__(self, db: Session = None):
        self.db = SessionLocal()

    async def find_one(self, id: ManagerId):
        user_orm = (
            self.db.query(UserModel)
            .filter(UserModel.id == id.id.__str__())
            .filter(UserModel.role == UserRole.MANAGER.name)
            .first()
        )
        if is_none(user_orm):
            return None
        return manager_factory(
            id=user_orm.id,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            email=user_orm.email,
        )

    async def find_all(self):
        users_orm = (
            self.db.query(UserModel).filter(UserModel == UserRole.MANAGER.name).all()
        )
        return [
            manager_factory(
                id=user_orm.id,
                first_name=user_orm.first_name,
                last_name=user_orm.last_name,
                email=user_orm.email,
            )
            for user_orm in users_orm
        ]

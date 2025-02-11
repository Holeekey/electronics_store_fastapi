from uuid import UUID
from src.common.domain.utils.is_none import is_none
from src.user.application.models.user import UserRole
from src.user.application.repositories.client_repository import IClientRepository
from sqlalchemy.orm import Session
from src.common.infrastructure.database.database import SessionLocal
from src.user.domain.client.factories.client_factory import client_factory
from src.user.domain.client.value_objects.client_id import ClientId
from src.user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel


class ClientRepositorySqlAlchemy(IClientRepository):
    def __init__(self, db: Session = None):
        self.db = db

    async def find_one(self, id: ClientId):

        user_orm = (
            self.db.query(UserModel)
            .filter(UserModel.id == id.id.__str__())
            .filter(UserModel.role == UserRole.CLIENT.name)
            .first()
        )
        if is_none(user_orm):
            return None
        return client_factory(
            id=user_orm.id,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            email=user_orm.email,
        )

    async def find_all(self):
        users_orm = (
            self.db.query(UserModel).filter(UserModel == UserRole.CLIENT.name).all()
        )
        return [
            client_factory(
                id=UUID(user_orm.id),
                first_name=user_orm.first_name,
                last_name=user_orm.last_name,
                email=user_orm.email,
            )
            for user_orm in users_orm
        ]

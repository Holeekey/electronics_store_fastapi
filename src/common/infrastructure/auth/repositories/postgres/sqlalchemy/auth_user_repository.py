from typing import Optional

from common.domain.utils.is_none import is_none
from common.infrastructure.auth.db_models.auth_user_model import AuthUserModel
from common.infrastructure.auth.models.auth_user import AuthUser
from sqlalchemy.orm import Session


class AuthUserRepositorySqlAlchemy:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, id: str) -> Optional[AuthUser]:
        user_orm = self.db.query(AuthUserModel).filter(AuthUserModel.id == id).first()
        if is_none(user_orm):
            return None
        return AuthUser(
            id=user_orm.id,
            username=user_orm.username,
            email=user_orm.email,
            role=user_orm.role,
            status=user_orm.status,
        )

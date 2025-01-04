from sqlalchemy import Column, ForeignKey, String, UUID
from src.common.infrastructure.database.database import Base
from src.user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel

class ShoppingCartModel(Base):
    __tablename__ = "shopping_cart"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
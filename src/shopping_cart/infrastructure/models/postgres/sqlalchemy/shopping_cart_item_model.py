from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UUID
from src.common.infrastructure.database.database import Base
from src.user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel

class ShoppingCartItemModel(Base):
    __tablename__ = "shopping_cart_items"
    __table_args__ = {"extend_existing": True}

    shopping_cart_id = Column(UUID, ForeignKey("shopping_cart.id"), primary_key=True, nullable=False)
    product_id = Column(String, ForeignKey("products.id"), primary_key=True, nullable=False)
    quantity = Column(Integer,nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    
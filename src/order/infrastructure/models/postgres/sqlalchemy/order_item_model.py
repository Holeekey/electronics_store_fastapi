from sqlalchemy import Column, ForeignKey, Integer, String, UUID
from src.common.infrastructure.database.database import Base

class OrderItemModel(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer,nullable=False)
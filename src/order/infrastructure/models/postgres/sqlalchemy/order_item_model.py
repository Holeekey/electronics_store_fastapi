from sqlalchemy import Column, Float, ForeignKey, Integer, String, UUID
from src.common.infrastructure.database.database import Base

class OrderItemModel(Base):
    __tablename__ = "order_items"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID, primary_key=True, index=True)
    order_id = Column(UUID, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Float,nullable=False)
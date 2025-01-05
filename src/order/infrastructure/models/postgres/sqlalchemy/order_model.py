from sqlalchemy import Column, DateTime, ForeignKey, String, UUID, Enum as SqlEnum
from src.order.domain.value_objects.order_status import OrderStatusOptions
from src.common.infrastructure.database.database import Base

class OrderModel(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(SqlEnum(OrderStatusOptions))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
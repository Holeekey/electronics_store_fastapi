from sqlalchemy import Integer, Column, String
from common.infrastructure.database.database import Base


class InventoryModel(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True, index=True)
    product_id = Column(String)
    stock = Column(Integer)

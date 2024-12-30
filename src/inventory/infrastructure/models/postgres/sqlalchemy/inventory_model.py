from sqlalchemy import INT, Column, ForeignKey, String
from common.infrastructure.database.database import Base


class InventoryModel(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True, index=True)
    product_id = Column(String ,ForeignKey('products.id'))
    stock = Column(INT)

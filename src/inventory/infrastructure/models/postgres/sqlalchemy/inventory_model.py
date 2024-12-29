from sqlalchemy import Column, ForeignKey, int, String
from common.infrastructure.database.database import Base


class ProductModel(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True, index=True)
    product_id = Column(ForeignKey('products.id'))
    stock = Column(int)

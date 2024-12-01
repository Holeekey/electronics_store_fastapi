from sqlalchemy import Column, String, Float, Int
from common.infrastructure.database.database import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    status = Column(Int)

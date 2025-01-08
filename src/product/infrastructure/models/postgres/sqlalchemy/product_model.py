from sqlalchemy import Column, String, Float, Integer, Text
from src.common.infrastructure.database.database import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    description = Column(Text)

    cost = Column(Float)
    margin = Column(Float)

    price = Column(Float)
    earning = Column(Float)

    status = Column(String)

    #to-do Add created_at, updated_at timestamps
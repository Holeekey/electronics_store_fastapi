from uuid import UUID
from sqlalchemy.orm import Session
from common.domain.result.result import Result
from common.domain.utils.is_none import is_none
from product.application.info.product_created_info import product_created_info
from product.application.repositories.product_repository import IProductRepository
from common.infrastructure.database.database import SessionLocal
from product.domain.factories.product_factory import product_factory
from product.domain.product import Product
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_name import ProductName
from product.infrastructure.models.postgres.sqlalchemy.product_model import ProductModel


class ProductRepositorySqlAlchemy(IProductRepository):
    def __init__(self):
        self.db: Session = SessionLocal()

    def map_model_to_product(self, product_orm: ProductModel):
        return product_factory(
            id=product_orm.id,
            name=product_orm.name,
            price=product_orm.price,
            status=product_orm.status
        )

    async def find_one(self, id: ProductId):
        product_orm = (
            self.db.query(ProductModel).filter(ProductModel.id == str(id.id)).first()
        )
        if is_none(product_orm):
            return None
        return self.map_model_to_product(product_orm)

    async def find_by_name(self, name: ProductName):
        product_orm = (
            self.db.query(ProductModel).filter(ProductModel.name == name.name).first()
        )
        if is_none(product_orm):
            return None
        return self.map_model_to_product(product_orm)

    async def save(self, product: Product):
        product_orm = ProductModel(
            id=product.id.id, name=product.name.name, price=product.price.price, status=product.status.status
        )
        self.db.add(product_orm)
        self.db.commit()
        self.db.refresh(product_orm)
        return Result.success(product, product_created_info())

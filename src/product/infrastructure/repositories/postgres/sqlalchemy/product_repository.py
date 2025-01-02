from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session
from src.common.domain.result.result import Result, result_info_factory
from src.common.domain.utils.is_none import is_none
from src.product.application.info.product_created_info import product_created_info
from src.product.application.repositories.product_repository import IProductRepository
from src.common.infrastructure.database.database import SessionLocal
from src.product.domain.factories.product_factory import product_factory
from src.product.domain.product import Product
from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_name import ProductName
from src.product.infrastructure.models.postgres.sqlalchemy.product_model import ProductModel


class ProductRepositorySqlAlchemy(IProductRepository):
    def __init__(self):
        self.db: Session = SessionLocal()

    def map_model_to_product(self, product_orm: ProductModel):
        return product_factory(
            id=product_orm.id,
            code = product_orm.code,
            name=product_orm.name,
            description=product_orm.description,
            cost=product_orm.cost,
            margin=product_orm.margin,
            status=product_orm.status
        )

    async def find_one(self, id: ProductId) -> Optional[Product]:
        product_orm = (
            self.db.query(ProductModel).filter(ProductModel.id == str(id.id)).filter(ProductModel.status != 0).first()
        )
        if is_none(product_orm):
            return None
        return self.map_model_to_product(product_orm)
    
    async def find_many(self, page:int = 1, per_page:int = 5) -> List[Product]:
        product_orm_list = (
            self.db.query(ProductModel).filter(ProductModel.status != 0).offset((page-1)*per_page).limit(per_page).all()
        )
        if is_none(product_orm_list):
            return None
        return [self.map_model_to_product(product_orm) for product_orm in product_orm_list]

    async def find_by_name(self, name: ProductName) -> Optional[Product]:
        product_orm = (
            self.db.query(ProductModel).filter(ProductModel.name == name.name).filter(ProductModel.status != 0).first()
        )
        if is_none(product_orm):
            return None
        return self.map_model_to_product(product_orm)

    async def save(self, product: Product) -> Result[Product]:
        product_orm = ProductModel(
            id=product.id.id, 
            code=product.code.code, 
            name=product.name.name, 
            description=product.description.description, 
            cost=product.pricing.cost, 
            margin=product.pricing.margin, 
            price=product.pricing.price, 
            earning=product.pricing.earning,
            status= product.status.status.value
        )
        self.db.add(product_orm)
        self.db.commit()
        self.db.refresh(product_orm)
        return Result.success(product, product_created_info())

    async def update(self, id: ProductId, new_product: Product) -> Result[Product]:
        target_product: ProductModel = self.db.query(ProductModel).filter(ProductModel.id == str(id.id)).first()
        if (is_none(target_product)):
            return Result.failure(Exception("Product not found"))
        if (target_product.status == 0): #Product is inactive
            return Result.failure(Exception("Product not found"))
        if (target_product.id != new_product.id.id):
            return Result.failure(ValueError("Target ID and ID of updated product do not match"))
        
        target_product.code = new_product.code.code
        target_product.name = new_product.name.name
        target_product.description = new_product.description.description
        target_product.cost = new_product.pricing.cost
        target_product.margin = new_product.pricing.margin
        target_product.price = new_product.pricing.price
        target_product.earning = new_product.pricing.earning
        target_product.status = new_product.status.status.value
        self.db.add(target_product)
        self.db.commit()
        self.db.refresh(target_product)
        info = result_info_factory("UPD-001", "Product updated successfully")
        return Result.success(new_product, info=info())

    async def delete(self, product: Product) -> Result[str]:
        target_product: ProductModel = self.db.query(ProductModel).filter(ProductModel.id == str(product.id.id)).first()
        if (is_none(target_product)):
            return Result.failure(Exception("Product not found"))
        if (target_product.status == 0): #Product is inactive
            return Result.failure(Exception("Product not found"))
        
        target_product.status = 0
        self.db.add(target_product)
        self.db.commit()
        self.db.refresh(target_product)

        info = result_info_factory("DEL-001","Product deactivated successfully")
        return Result.success("Product deactivated sucessfully", info=info())
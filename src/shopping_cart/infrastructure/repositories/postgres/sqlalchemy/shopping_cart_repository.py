import datetime
from typing import Optional
from sqlalchemy.orm import Session

from src.common.domain.utils.is_none import is_none
from src.shopping_cart.domain.factories.shopping_cart_factory import shopping_cart_factory
from src.shopping_cart.domain.factories.shopping_cart_item_factory import shopping_cart_item_factory
from src.shopping_cart.application.repositories.shopping_cart_repository import IShoppingCartRepository
from src.shopping_cart.domain.shopping_cart import ShoppingCart
from src.shopping_cart.infrastructure.models.postgres.sqlalchemy.shopping_cart_item_model import ShoppingCartItemModel
from src.shopping_cart.infrastructure.models.postgres.sqlalchemy.shopping_cart_model import ShoppingCartModel
from src.user.domain.client.value_objects.client_id import ClientId

class ShoppingCartRepositorySqlAlchemy(IShoppingCartRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def map_model_to_shopping_cart(self, shopping_cart_orm: ShoppingCartModel, shopping_cart_items_orm: list[ShoppingCartItemModel]):
        
        return shopping_cart_factory(
            id=str(shopping_cart_orm.id),
            client_id=shopping_cart_orm.user_id,
            items=[shopping_cart_item_factory(
                product_id=shopping_cart_item_orm.product_id,
                quantity=shopping_cart_item_orm.quantity,
            ) for shopping_cart_item_orm in shopping_cart_items_orm]
        )
        
    async def find_by_client_id(self, client_id: ClientId) -> Optional[ShoppingCart]:
        shopping_cart_orm = self.db.query(ShoppingCartModel).filter(ShoppingCartModel.user_id == str(client_id.id)).first()
        if is_none(shopping_cart_orm):
            return None
        shopping_cart_items_orm = self.db.query(ShoppingCartItemModel).filter(ShoppingCartItemModel.shopping_cart_id == shopping_cart_orm.id).all()
        return self.map_model_to_shopping_cart(shopping_cart_orm, shopping_cart_items_orm)
    
    async def save(self, shopping_cart: ShoppingCart) -> None:
        shopping_cart_orm = self.db.query(ShoppingCartModel).filter(ShoppingCartModel.id == shopping_cart.id.id).first()
        if is_none(shopping_cart_orm):
            shopping_cart_orm = ShoppingCartModel(
                id=shopping_cart.id.id,
                user_id=str(shopping_cart.client_id.id)
            )
            self.db.add(shopping_cart_orm)
            self.db.commit()
        
        shopping_cart_items_orm = self.db.query(ShoppingCartItemModel).filter(ShoppingCartItemModel.shopping_cart_id == shopping_cart.id.id)
        
        for item in shopping_cart.items:
            shopping_cart_item_orm = shopping_cart_items_orm.filter(ShoppingCartItemModel.product_id == item.product_id.id).first()
            if is_none(shopping_cart_item_orm):
                shopping_cart_item_orm = ShoppingCartItemModel(
                    shopping_cart_id=shopping_cart.id.id,
                    product_id=item.product_id.id,
                    quantity=item.quantity.quantity,
                    created_at=datetime.datetime.now()
                )
                self.db.add(shopping_cart_item_orm)
            elif shopping_cart_item_orm.quantity != item.quantity.quantity:
                shopping_cart_item_orm.quantity = item.quantity.quantity
                shopping_cart_item_orm.updated_at = datetime.datetime.now()
                self.db.add(shopping_cart_item_orm)
                
        for shopping_cart_item_orm in shopping_cart_items_orm:
            item_found = None
            for item in shopping_cart.items:
                if item.product_id.id == shopping_cart_item_orm.product_id:
                    item_found = item
                    break
            
            if is_none(item_found):
                self.db.delete(shopping_cart_item_orm)    
            
        self.db.commit()
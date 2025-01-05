
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.common.domain.utils.is_none import is_none
from src.order.domain.factories.order_factory import order_factory
from src.order.domain.factories.order_item_factory import order_item_factory
from src.order.domain.value_objects.order_id import OrderId
from src.order.infrastructure.models.postgres.sqlalchemy.order_item_model import OrderItemModel
from src.common.domain.utils.is_not_none import is_not_none
from src.order.infrastructure.models.postgres.sqlalchemy.order_model import OrderModel
from src.order.domain.order import Order
from src.order.application.repositories.order_repository import IOrderRepository

class OrderRepositorySqlAlchemy(IOrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def map_orm_to_order(self, order: OrderModel, order_items: list[OrderItemModel] ) -> Order:
        
        return order_factory(
            id=order.id,
            client_id=UUID(order.user_id),
            status=order.status,
            creation_date=order.created_at,
            items= [ 
                order_item_factory(
                    id= order_item.id,
                    product_id= order_item.product_id,
                    product_price= order_item.price,
                    quantity= order_item.quantity,
                )
                for order_item in order_items
            ]
        )
        

    async def find_one(self, order_id: OrderId) -> Optional[Order]:
        
        order_orm = self.db.query(OrderModel).filter(OrderModel.id == order_id.id).first()
        
        if is_none(order_orm):
            return None
        
        order_items_orm = self.db.query(OrderItemModel).filter(OrderItemModel.order_id == order_id.id).all()
        
        return self.map_orm_to_order(order_orm, order_items_orm)

    async def save(self, order: Order) -> None:
        
        order_orm = self.db.query(OrderModel).filter(OrderModel.id == order.id.id).first()
        
        if is_not_none(order_orm):
            order_orm.updated_at = datetime.now()
            order_orm.status = order._status.status.name
            self.db.add(order_orm)
            self.db.commit()
        else:
            order_orm = OrderModel(
                id = order.id.id,
                user_id = str(order._client_id.id),
                status = order._status.status.name,
                created_at = datetime.now()
            )
            self.db.add(order_orm)
            self.db.commit()
            
            for item in order._items:
                order_item_orm = OrderItemModel(
                    id = item.id.id,
                    order_id = order.id.id,
                    product_id = item.product_id.id,
                    quantity = item.quantity.quantity,
                    price = item.product_price.price,
                )
                self.db.add(order_item_orm)
            self.db.commit()
                
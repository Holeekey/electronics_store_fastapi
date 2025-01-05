
from datetime import datetime
from sqlalchemy.orm import Session

from order.infrastructure.models.postgres.sqlalchemy.order_item_model import OrderItemModel
from src.common.domain.utils.is_not_none import is_not_none
from src.order.infrastructure.models.postgres.sqlalchemy.order_model import OrderModel
from src.order.domain.order import Order
from src.order.application.repositories.order_repository import IOrderRepository

class OrderRepositorySqlAlchemy(IOrderRepository):
    def __init__(self, db: Session):
        self.db = db

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
                
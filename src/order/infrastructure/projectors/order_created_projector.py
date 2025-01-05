from bson import ObjectId
import jsonpickle
from src.order.domain.events.order_created import OrderCreated
from src.product.infrastructure.models.postgres.sqlalchemy.product_model import ProductModel
from src.common.infrastructure.database.database import get_session
from src.common.domain.utils.is_not_none import is_not_none
from src.common.infrastructure.database.mongo import get_mongo_client


def order_created_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    db_session = get_session().__next__()
    
    event: OrderCreated = jsonpickle.decode(body)
    
    db = mongo["template"]
    shop_cart_coll = db["order"]
    
    items_to_add = []
    
    for item in event.items:
        product = db_session.query(ProductModel).filter(ProductModel.id == item.product_id.id).first()
        items_to_add.append(
            {
                "order_item_id": str(item.id.id),
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "quantity": item.quantity.quantity,
                "unit_price": item._product_price.value,
                "total_price": item.quantity.quantity * item._product_price.value
            }
        )
        
    shop_cart_coll.insert_one({
        "_id": ObjectId(),
        "order_id": str(event.order_id.id),
        "user_id": str(event.client_id.id),
        "total_price": sum([item["total_price"] for item in items_to_add]),
        "status": "pending",
        "items": items_to_add
    })
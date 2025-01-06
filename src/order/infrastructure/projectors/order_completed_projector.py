from bson import ObjectId
import jsonpickle
from src.order.domain.events.order_completed import OrderCompleted
from src.product.infrastructure.models.postgres.sqlalchemy.product_model import ProductModel
from src.common.infrastructure.database.database import get_session
from src.common.domain.utils.is_not_none import is_not_none
from src.common.infrastructure.database.mongo import get_mongo_client


def order_completed_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    
    event: OrderCompleted = jsonpickle.decode(body)
    
    db = mongo["template"]
    shop_cart_coll = db["order"]
    
    filter = {"order_id": str(event.order_id.id)}
    
    update = {
        "$set": {
            "status": "completed",
        }
    }
    
    shop_cart_coll.update_one(filter, update, upsert=True)
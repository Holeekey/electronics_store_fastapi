from bson import ObjectId
import jsonpickle

from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.database.mongo import get_mongo_client
from src.product.domain.value_objects.product_status import ProductStatusOptions

def product_created_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    
    event = jsonpickle.decode(body)

    db = mongo["template"]
    product_coll = db["product"]
    product_coll.insert_one(
        {
            "_id": ObjectId(),
            "id": str(event.product_id.id),
            "code": str(event.product_code.code),
            "name": str(event.product_name.name),
            "description": str(event.product_description.description),
            "cost": float(event.product_pricing.cost),
            "margin": float(event.product_pricing.margin),
            "price": float(event.product_pricing.price),
            "earning": float(event.product_pricing.earning),
            "status": int(ProductStatusOptions.ACTIVE.value),
        }
    )
import jsonpickle
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.database.mongo import get_mongo_client
from src.product.domain.value_objects.product_status import ProductStatusOptions


def product_deleted_projector(ch, method, properties, body):
    mongo = get_mongo_client().__next__()
    
    event = jsonpickle.decode(body)
    
    db = mongo["template"]
    product_coll = db["product"]
    
    filter = {"id": str(event.product_id.id)}
    
    update = {
        "$set": {
            "status": int(ProductStatusOptions.INACTIVE.value)
        }
    }
    
    product_coll.update_one(filter, update, upsert=True)
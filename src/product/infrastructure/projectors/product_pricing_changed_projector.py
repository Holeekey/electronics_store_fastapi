import jsonpickle
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.database.mongo import get_mongo_client


def product_pricing_changed_projector(ch, method, properties, body):
    mongo = get_mongo_client().__next__()
    
    event = jsonpickle.decode(body)
    
    db = mongo["template"]
    product_coll = db["product"]
    
    filter = {"id": str(event.product_id.id)}
    
    update = {
        "$set": {
            "cost": float(event.product_pricing.cost),
            "margin": float(event.product_pricing.margin),
            "price": float(event.product_pricing.price),
            "earning": float(event.product_pricing.earning)
        }
    }
    
    product_coll.update_one(filter, update, upsert=True)
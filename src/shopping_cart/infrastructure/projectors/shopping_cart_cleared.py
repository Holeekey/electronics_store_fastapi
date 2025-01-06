import jsonpickle
from src.common.domain.utils.is_not_none import is_not_none
from src.common.infrastructure.database.mongo import get_mongo_client


def shopping_cart_cleared_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    
    event = jsonpickle.decode(body)
    
    db = mongo["template"]
    shop_cart_coll = db["shopping_cart"]
    
    cart = shop_cart_coll.find_one({"user_id": str(event.client_id.id)})
    
    if is_not_none(cart):
        
        shop_cart_coll.update_one(
            {"user_id": str(event.client_id.id)},
            {"$set": {"items": [], "total_price": 0.00}}
        )
import jsonpickle
from src.common.domain.utils.is_not_none import is_not_none
from src.common.infrastructure.database.mongo import get_mongo_client


def item_removed_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    
    event = jsonpickle.decode(body)
    
    db = mongo["template"]
    shop_cart_coll = db["shopping_cart"]
    
    cart = shop_cart_coll.find_one({"user_id": str(event.client_id.id)})
    
    if is_not_none(cart):
        cart_items = cart["items"]
        new_items = []
        for item in cart_items:
            if item["id"] != str(event.product_id.id):
                new_items.append(item)
        
        shop_cart_coll.update_one(
            {"user_id": str(event.client_id.id)},
            {"$set": {"items": new_items}}
        )
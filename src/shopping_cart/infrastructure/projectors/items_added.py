from bson import ObjectId
import jsonpickle
from src.common.domain.utils.is_none import is_none
from src.product.infrastructure.models.postgres.sqlalchemy.product_model import ProductModel
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.database.mongo import get_mongo_client


def items_added_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    db_session = get_session().__next__()
    
    event = jsonpickle.decode(body)
    
    db = mongo["template"]
    shop_cart_coll = db["shopping_cart"]
    
    items_to_add = []
    
    for item in event.items:
        product = db_session.query(ProductModel).filter(ProductModel.id == item.product_id.id).first()
        items_to_add.append(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "quantity": item.quantity.quantity,
            }
        )
    
    cart = shop_cart_coll.find_one({"user_id": str(event.client_id.id)})
    
    if is_none(cart):
        shop_cart_coll.insert_one(
            {
                "_id": ObjectId(),
                "user_id": str(event.client_id.id),
                "total_price": round(sum([item["price"] * item["quantity"] for item in items_to_add]),2),
                "items": items_to_add,
            }
        )
    else:
        old_items = cart["items"]
        new_items = []
        for item in items_to_add:
            item_found = None
            for old_item in old_items:
                if old_item["id"] == item["id"]:
                    item_found = old_item
                    break
            if item_found:
                item_found_index = old_items.index(item_found)
                old_items.pop(item_found_index)
                new_items.insert(item_found_index+1, item)
            else:
                new_items.append(item)
                
        shop_cart_coll.update_one(
            {"user_id": str(event.client_id.id)},
            {"$set": {"items": new_items, "total_price": round(sum([item["price"] * item["quantity"] for item in new_items]),2)}}
        )
        
    
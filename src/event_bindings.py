from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import EventBind

from src.order.domain.events.order_cancelled import ORDER_CANCELLED
from src.order.domain.events.order_completed import ORDER_COMPLETED
from src.order.domain.events.order_created import ORDER_CREATED
from src.order.infrastructure.projectors.order_created_projector import order_created_projector
from src.order.infrastructure.projectors.order_cancelled_projector import order_cancelled_projector
from src.order.infrastructure.projectors.order_completed_projector import order_completed_projector

from src.shopping_cart.domain.events.shopping_cart_cleared import SHOPPING_CART_CLEARED
from src.shopping_cart.infrastructure.projectors.shopping_cart_cleared import shopping_cart_cleared_projector
from src.shopping_cart.domain.events.shopping_cart_item_removed import SHOPPING_CART_ITEM_REMOVED
from src.shopping_cart.infrastructure.projectors.item_removed import item_removed_projector
from src.shopping_cart.domain.events.shopping_cart_items_added import SHOPPING_CART_ITEMS_ADDED
from src.shopping_cart.infrastructure.projectors.items_added import items_added_projector

from src.user.domain.client.events.client_activated import CLIENT_ACTIVATED
from src.user.domain.client.events.client_created import CLIENT_CREATED
from src.user.domain.client.events.client_email_changed import CLIENT_EMAIL_CHANGED
from src.user.domain.client.events.client_name_changed import CLIENT_NAME_CHANGED
from src.user.domain.client.events.client_suspended import CLIENT_SUSPENDED
from src.user.domain.manager.events.manager_activated import MANAGER_ACTIVATED
from src.user.domain.manager.events.manager_created import MANAGER_CREATED
from src.user.domain.manager.events.manager_email_changed import MANAGER_EMAIL_CHANGED
from src.user.domain.manager.events.manager_name_changed import MANAGER_NAME_CHANGED
from src.user.domain.manager.events.manager_suspended import MANAGER_SUSPENDED
from src.user.infrastructure.projectors.client_activated import client_activated_projector
from src.user.infrastructure.projectors.client_email_changed_projector import client_email_changed_projector
from src.user.infrastructure.projectors.client_name_changed import client_name_changed_projector
from src.user.infrastructure.projectors.client_suspended import client_suspended_projector
from src.user.infrastructure.projectors.manager_activated import manager_activated_projector
from src.user.infrastructure.projectors.manager_email_changed_projector import manager_email_changed_projector
from src.user.infrastructure.projectors.client_created_projector import client_created_projector
from src.user.infrastructure.projectors.manager_created_projector import manager_created_projector
from src.user.infrastructure.projectors.manager_name_changed import manager_name_changed_projector
from src.user.infrastructure.projectors.manager_suspended import manager_suspended_projector

from src.product.domain.events.product_created import PRODUCT_CREATED
from src.product.domain.events.product_code_changed import PRODUCT_CODE_CHANGED
from src.product.domain.events.product_name_changed import PRODUCT_NAME_CHANGED
from src.product.domain.events.product_description_changed import PRODUCT_DESCRIPTION_CHANGED
from src.product.domain.events.product_pricing_changed import PRODUCT_PRICING_CHANGED
from src.product.domain.events.product_deleted import PRODUCT_DELETED
from src.product.infrastructure.projectors.product_created_projector import product_created_projector
from src.product.infrastructure.projectors.product_code_changed_projector import product_code_changed_projector
from src.product.infrastructure.projectors.product_name_changed_projector import product_name_changed_projector
from src.product.infrastructure.projectors.product_description_changed_projector import product_description_changed_projector
from src.product.infrastructure.projectors.product_pricing_changed_projector import product_pricing_changed_projector
from src.product.infrastructure.projectors.product_deleted_projector import product_deleted_projector

event_bindings = [
    EventBind(name=CLIENT_CREATED, handler=client_created_projector),
    EventBind(name=CLIENT_NAME_CHANGED, handler=client_name_changed_projector),
    EventBind(name=CLIENT_EMAIL_CHANGED, handler=client_email_changed_projector),
    EventBind(name=CLIENT_SUSPENDED, handler=client_suspended_projector),
    EventBind(name=CLIENT_ACTIVATED, handler=client_activated_projector),
    EventBind(name=MANAGER_CREATED, handler=manager_created_projector),
    EventBind(name=MANAGER_NAME_CHANGED, handler=manager_name_changed_projector),
    EventBind(name=MANAGER_EMAIL_CHANGED, handler=manager_email_changed_projector),
    EventBind(name=MANAGER_SUSPENDED, handler=manager_suspended_projector),
    EventBind(name=MANAGER_ACTIVATED, handler=manager_activated_projector),
    EventBind(name=SHOPPING_CART_ITEMS_ADDED, handler=items_added_projector),
    EventBind(name=SHOPPING_CART_ITEM_REMOVED, handler=item_removed_projector),
    EventBind(name=SHOPPING_CART_CLEARED, handler=shopping_cart_cleared_projector),
    EventBind(name=PRODUCT_CREATED, handler=product_created_projector),
    EventBind(name=PRODUCT_CODE_CHANGED, handler=product_code_changed_projector),
    EventBind(name=PRODUCT_NAME_CHANGED, handler=product_name_changed_projector),
    EventBind(name=PRODUCT_DESCRIPTION_CHANGED, handler=product_description_changed_projector),
    EventBind(name=PRODUCT_PRICING_CHANGED, handler=product_pricing_changed_projector),
    EventBind(name=PRODUCT_DELETED, handler=product_deleted_projector),
    EventBind(name=ORDER_CREATED, handler=order_created_projector),
    EventBind(name=ORDER_CANCELLED, handler=order_cancelled_projector),
    EventBind(name=ORDER_COMPLETED, handler=order_completed_projector),
]
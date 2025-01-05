from src.order.domain.events.order_created import ORDER_CREATED
from src.order.infrastructure.projectors.order_created_projector import order_created_projector
from src.shopping_cart.domain.events.shopping_cart_cleared import SHOPPING_CART_CLEARED
from src.shopping_cart.infrastructure.projectors.shopping_cart_cleared import shopping_cart_cleared_projector
from src.shopping_cart.domain.events.shopping_cart_item_removed import SHOPPING_CART_ITEM_REMOVED
from src.shopping_cart.infrastructure.projectors.item_removed import item_removed_projector
from src.shopping_cart.domain.events.shopping_cart_items_added import SHOPPING_CART_ITEMS_ADDED
from src.shopping_cart.infrastructure.projectors.items_added import items_added_projector
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import EventBind
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
    EventBind(name=ORDER_CREATED, handler=order_created_projector)
]
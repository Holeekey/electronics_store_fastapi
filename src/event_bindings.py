from common.infrastructure.rabbitmq.rabbitmq_event_handler import EventBind
from user.domain.client.events.client_created import CLIENT_CREATED
from user.domain.manager.events.manager_created import MANAGER_CREATED
from user.infrastructure.projectors.client_created_projector import client_created_projector
from user.infrastructure.projectors.manager_created_projector import manager_created_projector

event_bindings = [
    EventBind(name=CLIENT_CREATED, handler=client_created_projector),
    EventBind(name=MANAGER_CREATED, handler=manager_created_projector)
]
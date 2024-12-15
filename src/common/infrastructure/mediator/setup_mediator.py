from common.infrastructure.mediator.setup_di import setup_di
from diator.mediator import Mediator
from diator.requests import RequestMap
from diator.events import EventMap, EventEmitter
from diator.message_brokers.redis import RedisMessageBroker

# from redis import asyncio

from config import REDIS_URL
from user.infrastructure.command_handlers.create_user_command_handler import (
    CreateUserCommandHandler,
)
from user.infrastructure.commands.create_user_command import CreateUserCommand
from user.infrastructure.events.user_created.manager_created import ManagerCreatedDiator
from user.infrastructure.projectors.manager_created_projector import (
    ManagerCreatedProjector,
)


def setup_mediator() -> Mediator:

    container = setup_di()

    request_map = RequestMap()
    request_map.bind(CreateUserCommand, CreateUserCommandHandler)

    event_map = EventMap()
    event_map.bind(ManagerCreatedDiator, ManagerCreatedProjector)

    # redis_client = asyncio.Redis.from_url(f"{REDIS_URL}/0")

    event_emitter = EventEmitter(event_map, message_broker=None, container=container)

    return Mediator(
        container=container, request_map=request_map, event_emitter=event_emitter
    )


mediator = setup_mediator()


def get_mediator():
    try:
        yield mediator
    finally:
        # Aquí puedes realizar cualquier limpieza necesaria
        pass

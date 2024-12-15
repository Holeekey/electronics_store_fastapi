from diator.container.di import DIContainer
from di import Container, bind_by_type
from di.dependent import Dependent

from common.infrastructure.cryptography.fernetCryptography_provider import (
    FernetProvider,
)
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from user.infrastructure.command_handlers.create_user_command_handler import (
    CreateUserCommandHandler,
)
from user.infrastructure.projectors.manager_created_projector import (
    ManagerCreatedProjector,
)

from user.infrastructure.queries.find_one.find_one_user_query_handler import (
    FindOneUserQueryHandler
)

from diator.mediator import Mediator
from diator.requests import RequestMap
from diator.events import EventMap, EventEmitter
from diator.middlewares import MiddlewareChain

from common.infrastructure.middlewares.diator.logging_middleware import LoggingMiddleware

# from redis import asyncio

from user.infrastructure.command_handlers.create_user_command_handler import (
    CreateUserCommandHandler,
)
from user.infrastructure.commands.create_user_command import CreateUserCommand
from user.infrastructure.events.user_created.manager_created import ManagerCreatedDiator
from user.infrastructure.projectors.manager_created_projector import (
    ManagerCreatedProjector,
)
from user.infrastructure.queries.find_one.find_one_user_query_handler import FindOneUserQueryHandler
from user.infrastructure.queries.find_one.types.query import FindOneUserQuery

def setup_di() -> DIContainer:
    external_container = Container()

    external_container.solve(
        Dependent(
            UUIDGenerator,
            scope="singleton",
        ),
        scopes=["singleton"],
    )

    external_container.solve(
        Dependent(
            FernetProvider,
            scope="singleton",
        ),
        scopes=["singleton"],
    )

    external_container.bind(
        bind_by_type(
            Dependent(
                CreateUserCommandHandler,
                scope="request",
            ),
            CreateUserCommandHandler,
        )
    )
    
    external_container.bind(
        bind_by_type(
            Dependent(
                FindOneUserQueryHandler,
                scope="request",
            ),
            FindOneUserQueryHandler,
        )
    )

    external_container.bind(
        bind_by_type(
            Dependent(
                ManagerCreatedProjector,
                scope="request",
            ),
            ManagerCreatedProjector,
        )
    )

    container = DIContainer()
    container.attach_external_container(external_container)

    return container

def setup_mediator() -> Mediator:

    container = setup_di()

    request_map = RequestMap()
    request_map.bind(CreateUserCommand, CreateUserCommandHandler)
    request_map.bind(FindOneUserQuery, FindOneUserQueryHandler)

    event_map = EventMap()
    event_map.bind(ManagerCreatedDiator, ManagerCreatedProjector)

    # redis_client = asyncio.Redis.from_url(f"{REDIS_URL}/0")

    event_emitter = EventEmitter(event_map, message_broker=None, container=container)

    middleware_chain = MiddlewareChain()
    middleware_chain.add(LoggingMiddleware())

    return Mediator(
        container=container,
        request_map=request_map,
        event_emitter=event_emitter,
        middleware_chain=middleware_chain,
    )


mediator = setup_mediator()


def get_mediator():
    try:
        yield mediator
    finally:
        # Aquí puedes realizar cualquier limpieza necesaria
        pass

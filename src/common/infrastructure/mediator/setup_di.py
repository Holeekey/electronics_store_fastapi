from diator.container.di import DIContainer
from di import Container, bind_by_type
from di.dependent import Dependent

from common.infrastructure.cryptography.fernetCryptography_provider import (
    FernetProvider,
)
from common.infrastructure.database.database import get_session
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

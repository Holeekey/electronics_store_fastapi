from common.infrastructure.mediator.setup_di import setup_di
from diator.mediator import Mediator
from diator.requests import RequestMap

from user.infrastructure.command_handlers.create_user_command_handler import CreateUserCommandHandler
from user.infrastructure.commands.create_user_command import CreateUserCommand

def setup_mediator() -> Mediator:
    
    container = setup_di()
    
    request_map = RequestMap()
    request_map.bind(CreateUserCommand, CreateUserCommandHandler)
        
    return Mediator(
        container=container,
        request_map=request_map
    )
    
mediator = setup_mediator()
    
def get_mediator():
    try:
        yield mediator
    finally:
        # Aquí puedes realizar cualquier limpieza necesaria
        pass

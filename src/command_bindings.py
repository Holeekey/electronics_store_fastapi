from common.infrastructure.bus.bus import Bind
from user.infrastructure.command_handlers.create_user_command_handler import create_user_command_handler
from user.infrastructure.routes.types.create.create_user_dto import CreateUserDto

command_bus_bindings = [
    Bind(CreateUserDto, create_user_command_handler)
]
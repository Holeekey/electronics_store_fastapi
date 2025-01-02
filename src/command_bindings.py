from common.infrastructure.bus.bus import Bind
from user.application.commands.delete_manager.types.dto import DeleteManagerDto
from user.application.commands.update.types.dto import UpdateUserDto
from user.infrastructure.command_handlers.create_user_command_handler import create_user_command_handler
from user.infrastructure.command_handlers.delete_manager_command_handler import delete_manager_command_handler
from user.infrastructure.command_handlers.update_user_command_handler import update_user_command_handler
from user.infrastructure.routes.types.create.create_user_dto import CreateUserDto

command_bus_bindings = [
    Bind(CreateUserDto, create_user_command_handler),
    Bind(UpdateUserDto, update_user_command_handler),
    Bind(DeleteManagerDto, delete_manager_command_handler),
]
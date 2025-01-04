from src.shopping_cart.application.services.remove_item.types.dto import RemoveItemFromShoppingCartDto
from src.shopping_cart.infrastructure.command_handlers.remove_item_from_shopping_cart_command_handler import remove_item_from_shopping_cart_command_handler
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartDto
from src.shopping_cart.infrastructure.command_handlers.add_items_to_shopping_cart_command_handler import add_items_to_shopping_cart_command_handler
from src.common.infrastructure.bus.bus import Bind
from src.user.application.commands.delete_manager.types.dto import DeleteManagerDto
from src.user.application.commands.update.types.dto import UpdateUserDto
from src.user.infrastructure.command_handlers.create_user_command_handler import create_user_command_handler
from src.user.infrastructure.command_handlers.delete_manager_command_handler import delete_manager_command_handler
from src.user.infrastructure.command_handlers.update_user_command_handler import update_user_command_handler
from src.user.infrastructure.routes.types.create.create_user_dto import CreateUserDto

command_bus_bindings = [
    Bind(CreateUserDto, create_user_command_handler),
    Bind(UpdateUserDto, update_user_command_handler),
    Bind(DeleteManagerDto, delete_manager_command_handler),
    Bind(AddItemsToShoppingCartDto, add_items_to_shopping_cart_command_handler),
    Bind(RemoveItemFromShoppingCartDto, remove_item_from_shopping_cart_command_handler),
]
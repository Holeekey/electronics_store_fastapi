from src.common.infrastructure.bus.bus import Bind

from src.shopping_cart.application.services.remove_item.types.dto import RemoveItemFromShoppingCartDto
from src.shopping_cart.infrastructure.command_handlers.remove_item_from_shopping_cart_command_handler import remove_item_from_shopping_cart_command_handler
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartDto
from src.shopping_cart.infrastructure.command_handlers.add_items_to_shopping_cart_command_handler import add_items_to_shopping_cart_command_handler

from src.user.application.commands.delete_manager.types.dto import DeleteManagerDto
from src.user.application.commands.update.types.dto import UpdateUserDto
from src.user.infrastructure.command_handlers.create_user_command_handler import create_user_command_handler
from src.user.infrastructure.command_handlers.delete_manager_command_handler import delete_manager_command_handler
from src.user.infrastructure.command_handlers.update_user_command_handler import update_user_command_handler
from src.user.infrastructure.routes.types.create.create_user_dto import CreateUserDto

from src.product.infrastructure.routes.types.create_product_dto import CreateProductDto
from src.product.infrastructure.command_handlers.create_product_command_handler import create_product_command_handler
from src.product.application.commands.update.types.dto import UpdateProductDto
from src.product.infrastructure.command_handlers.update_product_command_handler import update_product_command_handler
from src.product.infrastructure.routes.types.delete_product_dto import DeleteProductDto
from src.product.infrastructure.command_handlers.delete_product_command_handler import delete_product_command_handler

command_bus_bindings = [
    Bind(CreateUserDto, create_user_command_handler),
    Bind(UpdateUserDto, update_user_command_handler),
    Bind(DeleteManagerDto, delete_manager_command_handler),
    Bind(AddItemsToShoppingCartDto, add_items_to_shopping_cart_command_handler),
    Bind(RemoveItemFromShoppingCartDto, remove_item_from_shopping_cart_command_handler),
    Bind(CreateProductDto, create_product_command_handler),
    Bind(UpdateProductDto, update_product_command_handler),
    Bind(DeleteProductDto, delete_product_command_handler)
]
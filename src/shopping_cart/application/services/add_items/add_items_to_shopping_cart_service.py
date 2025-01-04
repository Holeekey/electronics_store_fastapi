from uuid import UUID
from src.shopping_cart.domain.value_objects.shopping_cart_id import ShoppingCartId
from src.common.application.events.event_handlers import IEventPublisher
from src.common.application.id_generator.id_generator import IDGenerator
from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result
from src.common.domain.utils.is_none import is_none
from src.product.application.repositories.product_repository import IProductRepository
from src.product.domain.value_objects.product_id import ProductId
from src.shopping_cart.application.info.add_items_to_shopping_cart_info import add_items_to_shopping_cart_info
from src.shopping_cart.application.repositories.shopping_cart_repository import IShoppingCartRepository
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartCommand
from src.shopping_cart.application.services.add_items.types.response import AddItemsToShoppingCartResponse
from src.shopping_cart.application.errors.product_not_found import product_not_found_error
from src.shopping_cart.application.errors.client_not_found import client_not_found_error
from src.shopping_cart.domain.factories.shopping_cart_item_factory import shopping_cart_item_factory
from src.shopping_cart.domain.shopping_cart import ShoppingCart
from src.user.application.repositories.client_repository import IClientRepository
from src.user.domain.client.value_objects.client_id import ClientId


class AddItemsToShoppingCartService(IApplicationService):
    
    def __init__(
        self,
        id_generator: IDGenerator,
        client_repository: IClientRepository,
        product_repository: IProductRepository,
        shopping_cart_repository: IShoppingCartRepository,
        event_publisher: IEventPublisher
    ):
        self.id_generator = id_generator
        self.client_repository = client_repository
        self.product_repository = product_repository
        self.shopping_cart_repository = shopping_cart_repository
        self.event_publisher = event_publisher
    
    async def execute(self, data: AddItemsToShoppingCartCommand) -> Result[AddItemsToShoppingCartResponse]:
        
        client_id = ClientId(UUID(data.client_id))
        
        client = await self.client_repository.find_one(client_id)
        
        if is_none(client):
            return Result.failure(client_not_found_error())
        
        for item in data.items:
            product = await self.product_repository.find_one(ProductId(item.product_id))
            if is_none(product):
                return Result.failure(product_not_found_error())
        
        shopping_cart = await self.shopping_cart_repository.find_by_client_id(client_id)
        
        if is_none(shopping_cart):
            shopping_cart = ShoppingCart(
                id=ShoppingCartId(UUID(self.id_generator.generate())),
                client_id=client_id,
                items=[]
            )
        
        items = [shopping_cart_item_factory(
            item.product_id,
            item.quantity
        ) for item in data.items]
        
        shopping_cart.add_items(items)
        
        await self.shopping_cart_repository.save(shopping_cart)
        
        # self.event_publisher.publish(shopping_cart.pull_events())
        
        return Result.success(AddItemsToShoppingCartResponse('Succesful'), add_items_to_shopping_cart_info())
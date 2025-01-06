
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.inventory.application.commands.create.create_inventory_command import CreateOrUpdateInventoryCommand
from src.inventory.application.commands.types.create_inventory_dto import CreateInventoryDto
from src.inventory.infrastructure.repositories.postgres.sqlalchemy.inventory_repository import InventoryRepositorySqlAlchemy
from src.order.application.services.create.create_order_service import CreateOrderService
from src.order.application.services.create.types.dto import CreateOrderDto
from src.order.domain.services.create_order_domain_service import CreateOrderDomainService
from src.order.infrastructure.repositories.postgres.sqlalchemy.order_repository import OrderRepositorySqlAlchemy
from src.shopping_cart.application.services.add_items.add_items_to_shopping_cart_service import AddItemsToShoppingCartService
from src.shopping_cart.application.services.add_items.types.dto import AddItemsToShoppingCartDto, ItemDetail
from src.shopping_cart.infrastructure.repositories.postgres.sqlalchemy.shopping_cart_repository import ShoppingCartRepositorySqlAlchemy
from src.product.application.commands.create.create_product_command import CreateProductCommand
from src.product.infrastructure.repositories.postgres.sqlalchemy.product_repository import ProductRepositorySqlAlchemy
from src.seed.data.product_data import product_data
from src.common.domain.result.result import Result, result_info_factory
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.common.application.decorators.error_decorator import ErrorDecorator
from src.common.infrastructure.cryptography.fernet.fernet_cryptography_provider import get_fernet_provider
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.events.rabbitmq.rabbitmq_event_handler import get_rabbit_mq_event_publisher
from src.common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.seed.data.user_data import user_data
from src.common.infrastructure.auth.db_models.auth_user_model import AuthUserRole
from src.common.infrastructure.auth.models.auth_user import AuthUser
from src.common.infrastructure.auth.role_checker import role_checker
from src.user.application.commands.create.create_user_command import CreateUserCommand
from src.user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy
from src.user.infrastructure.repositories.postgres.sqlalchemy.client_repository import ClientRepositorySqlAlchemy


seed_router = APIRouter(
    prefix="/seed",
    tags=["Seed"],
    responses={404: {"description": "Not found"}},
)


@seed_router.post("")
async def seed(
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.ADMIN]))],
):
    
    session = get_session().__next__()
    id_generator = UUIDGenerator()
    event_publisher = await get_rabbit_mq_event_publisher().__anext__()
    cryptography_provider = get_fernet_provider()
    user_repo = UserRepositorySqlAlchemy(session)
    client_repo = ClientRepositorySqlAlchemy(session)
    product_repo = ProductRepositorySqlAlchemy(session)
    inventory_repo = InventoryRepositorySqlAlchemy(session)
    shopping_cart_repo = ShoppingCartRepositorySqlAlchemy(session)
    order_repo = OrderRepositorySqlAlchemy(session)
    
    try:
        
        create_user_service = ErrorDecorator(
            service= CreateUserCommand(
                id_generator=id_generator,
                user_repository=user_repo,
                cryptography_provider=cryptography_provider,
                event_publisher=event_publisher,
            ),
            error_handler=error_response_handler
        )

        user_ids = []

        for user in user_data:
            result = await create_user_service.execute(user)
            user_ids.append(result.unwrap().user_id)
        
        create_product_service = ErrorDecorator(
            service= CreateProductCommand(
                id_generator=id_generator,
                product_repository= product_repo,
            ),
            error_handler=error_response_handler
        )
        
        product_ids = []
        
        for product in product_data:
            result = await create_product_service.execute(product)
            product_ids.append(result.unwrap().product_id)
        
        create_stock_service = ErrorDecorator(
            service= CreateOrUpdateInventoryCommand(
                id_generator=id_generator,
                inventory_repository= inventory_repo,
                product_repository= product_repo,
            ),
            error_handler=error_response_handler
        )
        
        for product_id in product_ids:
            await create_stock_service.execute(
                CreateInventoryDto(
                    product_id=product_id,
                    stock=20,
                )
            )
        
        add_items_to_cart_service = ErrorDecorator(
            service= AddItemsToShoppingCartService(
                id_generator=id_generator,
                product_repository= product_repo,
                client_repository= client_repo,
                shopping_cart_repository= shopping_cart_repo,
                event_publisher= event_publisher,
            ),
            error_handler=error_response_handler
        )
        
        shopping_cart_1 = AddItemsToShoppingCartDto(
            client_id=user_ids[0],
            items=[
                ItemDetail(
                    product_id=product_ids[0],
                    quantity=1,
                ),
                ItemDetail(
                    product_id=product_ids[1],
                    quantity=4,
                ),
                ItemDetail(
                    product_id=product_ids[2],
                    quantity=4,
                ),
                ItemDetail(
                    product_id=product_ids[3],
                    quantity=6,
                ),
            ]
        )
        
        await add_items_to_cart_service.execute(shopping_cart_1)
        
        shopping_cart_2 = AddItemsToShoppingCartDto(
            client_id=user_ids[1],
            items=[
                ItemDetail(
                    product_id=product_ids[3],
                    quantity=2,
                ),
                ItemDetail(
                    product_id=product_ids[7],
                    quantity=6,
                ),
                ItemDetail(
                    product_id=product_ids[2],
                    quantity=10,
                ),
            ]
        )
        
        await add_items_to_cart_service.execute(shopping_cart_2)
        
        shopping_cart_3 = AddItemsToShoppingCartDto(
            client_id=user_ids[2],
            items=[
                ItemDetail(
                    product_id=product_ids[6],
                    quantity=1,
                ),
                ItemDetail(
                    product_id=product_ids[10],
                    quantity=2,
                ),
                ItemDetail(
                    product_id=product_ids[11],
                    quantity=5,
                ),
            ]
        )
        
        await add_items_to_cart_service.execute(shopping_cart_3)
        
        order_create_service = ErrorDecorator(
            service= CreateOrderService(
                client_repository= client_repo,
                create_order_service= CreateOrderDomainService(product_repo),
                order_repository= order_repo,
                shopping_cart_repository= shopping_cart_repo,
                inventory_repository= inventory_repo,
                event_publisher= event_publisher,
            ),
            error_handler=error_response_handler
        )
        
        await order_create_service.execute(CreateOrderDto(user_ids[0]))
        await order_create_service.execute(CreateOrderDto(user_ids[1]))
        await order_create_service.execute(CreateOrderDto(user_ids[2]))
        
        shopping_cart_4 = AddItemsToShoppingCartDto(
            client_id=user_ids[2],
            items=[
                ItemDetail(
                    product_id=product_ids[6],
                    quantity=3,
                ),
                ItemDetail(
                    product_id=product_ids[1],
                    quantity=1,
                ),
                ItemDetail(
                    product_id=product_ids[0],
                    quantity=4,
                ),
            ]
        )
        
        await add_items_to_cart_service.execute(shopping_cart_4)
        
        await order_create_service.execute(CreateOrderDto(user_ids[2]))
        
        seed_info = result_info_factory(
            code="SEED-001", message="Seed executed succesfully"
        )
        
        result = Result.success(
            value={"message":"Succesful"},
            info=seed_info(),
        )
            
        return result.handle_success(handler=success_response_handler)
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"code": "SEED-E-001" ,"message": "Unable to execute seed. Seed already executed"})
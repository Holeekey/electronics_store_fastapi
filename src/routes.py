from fastapi import APIRouter

from src.order.infrastructure.routes.routes import order_router
from src.user.infrastructure.routes.routes import user_router
from src.product.infrastructure.routes.routes import product_router
from src.inventory.infrastructure.routes.routes import inventory_router
from src.shopping_cart.infrastructure.routes.routes import shopping_cart_router

router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)
router.include_router(inventory_router)
router.include_router(shopping_cart_router)

router.include_router(order_router)

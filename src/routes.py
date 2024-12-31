from fastapi import APIRouter
from src.user.infrastructure.routes.routes import user_router
from src.product.infrastructure.routes.routes import product_router

router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)

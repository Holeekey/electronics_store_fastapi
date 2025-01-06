from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.common.domain.utils.is_none import is_none
from src.common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from src.common.domain.result.result import Result, result_info_factory
from src.common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from src.order.infrastructure.models.postgres.sqlalchemy.order_model import OrderModel
from src.product.infrastructure.models.postgres.sqlalchemy.product_model import ProductModel
from src.order.infrastructure.models.postgres.sqlalchemy.order_item_model import OrderItemModel
from src.common.infrastructure.auth.db_models.auth_user_model import AuthUserRole
from src.common.infrastructure.auth.models.auth_user import AuthUser
from src.common.infrastructure.auth.role_checker import role_checker
from src.common.infrastructure.database.database import get_session
from src.user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel

report_router = APIRouter(
    prefix="/reports",
    tags=["Report"],
    responses={404: {"description": "Not found"}},
)

from src.common.application.error.application_error import application_error_factory

product_not_found_error = application_error_factory(
    code="RP-E-001", message="Product not found"
)

@report_router.get("/sales/totals")
async def get_sales_totals(
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    session: Annotated[Session, Depends(get_session)],
):
    order_count = session.query(OrderModel).count()
    order_items = session.query(OrderItemModel).all()
    
    sales_total_info = result_info_factory(
            code="RP-001", message="Sales reported successfully"
        )
        
    result = Result.success(
        value= {
            "total_sales_quantity": order_count,
            "total_sales": round(sum([item.price * item.quantity for item in order_items]),2)
        },
        info= sales_total_info(),
    )
        
    return result.handle_success(handler=success_response_handler)

@report_router.get("/sales/{product_id}")
async def get_product_sales(
    product_id: UUID,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    session: Annotated[Session, Depends(get_session)],
):
    product = session.query(ProductModel).filter(ProductModel.id == str(product_id)).first()
    
    if is_none(product):
        error = product_not_found_error()
        raise error_response_handler(error)
    
    query = session.query(OrderItemModel).filter(OrderItemModel.product_id == str(product_id))
    
    order_items = query.all()
    
    product_sales_info = result_info_factory(
            code="RP-002", message="Product sales reported successfully"
        )
        
    result = Result.success(
        value= {
            "orders_with_product": query.count(),
            "total_product_sales_quantity": round(sum([item.quantity for item in order_items]),2),
            "total_product_sales": round(sum([item.price * item.quantity for item in order_items]),2),
        },
        info= product_sales_info(),
    )
        
    return result.handle_success(handler=success_response_handler)
    
    
        

@report_router.get("/profit/totals")
async def get_profit_totals(
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    session: Annotated[Session, Depends(get_session)],
):
    products = session.query(ProductModel).all()
    order_items = session.query(OrderItemModel).all()
    
    profit = 0
    
    for item in order_items:
        product = None
        for p in products:
            if p.id == item.product_id:
                product = p
                break
        profit += item.quantity * (item.price - product.cost)
        
    product_profit_info = result_info_factory(
            code="RP-003", message="Total profit reported successfully"
    )
        
    result = Result.success(
        value= {
            "total_profit": round(profit,2),
        },
        info= product_profit_info(),
    )
        
    return result.handle_success(handler=success_response_handler)
    
    

@report_router.get("/profit/{product_id}")
async def get_product_profit(
    product_id: UUID,
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    session: Annotated[Session, Depends(get_session)],
):
    product = session.query(ProductModel).filter(ProductModel.id == str(product_id)).first()
    order_items = session.query(OrderItemModel).filter(OrderItemModel.product_id == str(product_id)).all()
        
    product_profit_info = result_info_factory(
            code="RP-004", message="Product profit reported successfully"
    )
        
    result = Result.success(
        value= {
            "total_profit": round(
                sum([ item.quantity*(item.price - product.cost) for item in order_items]),
                2
            ),
        },
        info= product_profit_info(),
    )
        
    return result.handle_success(handler=success_response_handler)

@report_router.get("/products/top")
async def get_top_products(
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    session: Annotated[Session, Depends(get_session)],
):
    
    products = session.query(ProductModel).all()
    order_items = session.query(OrderItemModel).all()
    
    class ProductSales:
        
        product: ProductModel
        quantity: int
        
        def __init__(self, product: ProductModel, quantity: int):
            self.product = product
            self.quantity = quantity
            
    product_sales: list[ProductSales] = []
    
    for product in products:
        product_sales.append(
            ProductSales(
                product,
                sum([item.quantity for item in order_items if item.product_id == product.id])
            )
        )
        
    product_sales.sort(key=lambda x: x.quantity, reverse=True)
    
    product_sales = product_sales[:5]
    
    top_products_info = result_info_factory(
            code="RP-005", message="Top products reported successfully"
    )
        
    result = Result.success(
        value= {
            "top_products": [
                {
                    "id": product.product.id,
                    "name": product.product.name,
                    "description": product.product.description,
                    "code": product.product.code,
                    "cost": product.product.cost,
                    "price": round(product.product.price,2),
                    "margin": f"{product.product.margin*100}%",
                    "quantity_sold": product.quantity,
                    "total_sales": round(product.quantity * product.product.price, 2),
                    "total_profict": round(product.quantity * (product.product.price - product.product.cost), 2)
                } for product in product_sales
            ]
        },
        info= top_products_info(),
    )
        
    return result.handle_success(handler=success_response_handler)
    

@report_router.get("/costumers/top")
async def get_top_costumers(
    _: Annotated[AuthUser, Depends(role_checker([AuthUserRole.MANAGER]))],
    session: Annotated[Session, Depends(get_session)],
):
    
    clients = session.query(UserModel).filter(UserModel.role == "CLIENT").all()
    
    order_items = session.query(OrderItemModel).join(OrderModel).all()
    
    class ClientSales:
        client: UserModel
        total_spent: int
        order_quantity: int
        
        def __init__(self, client: UserModel, total_spent: float, order_quantity: int):
            self.client = client
            self.total_spent = total_spent
            self.order_quantity = order_quantity
            
    client_sales: list[ClientSales] = []
    
    for client in clients:
        client_sales.append(
            ClientSales(
                client,
                sum([item.quantity * item.price for item in order_items if session.query(OrderModel).filter(OrderModel.id == item.order_id).first().user_id == client.id]),
                session.query(OrderModel).filter(OrderModel.user_id == client.id).count()
            )
        )
        
    client_sales.sort(key=lambda x: x.total_spent, reverse=True)
    
    client_sales = client_sales[:3]
    
    top_costumers_info = result_info_factory(
            code="RP-006", message="Top costumers reported successfully"
    )
        
    result = Result.success(
        value= {
            "top_products": [
                {
                    "id": client.client.id,
                    "name": f"{client.client.first_name} {client.client.last_name}",
                    "total_spent": round(client.total_spent, 2),
                    "total_orders": client.order_quantity,
                } for client in client_sales
            ]
        },
        info= top_costumers_info(),
    )
    
    return result.handle_success(handler=success_response_handler)
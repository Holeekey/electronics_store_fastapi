from dataclasses import dataclass
from datetime import datetime

@dataclass
class OrderItemResponse:
    id: str
    product_name: str
    total_price: float
    quantity: int

@dataclass
class CreateOrderReponse:
    order_id: str
    creation_date: datetime
    total_price: float
    items: OrderItemResponse
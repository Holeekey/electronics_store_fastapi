from dataclasses import dataclass
from src.common.application.service.application_service import IApplicationService

@dataclass
class ItemDetail:
    product_id: str
    quantity: int

@dataclass
class AddItemsToShoppingCartDto():
    client_id: str
    items: list[ItemDetail]
    
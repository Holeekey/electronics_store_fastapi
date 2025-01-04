from dataclasses import dataclass


@dataclass
class RemoveItemFromShoppingCartDto:
    product_id: str
    client_id: str
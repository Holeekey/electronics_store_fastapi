
from uuid import UUID


class CreateInventoryDto:
    def __init__(
        self,
        product_id: UUID,
        stock: int,
    ):
        self.productId = product_id
        self.stock = stock

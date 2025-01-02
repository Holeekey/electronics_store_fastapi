
from uuid import UUID


class AdjustInventoryDto:
    def __init__(
        self,
        product_id: UUID,
        stock_change: int,
    ):
        self.product_id = product_id
        self.stock = stock_change

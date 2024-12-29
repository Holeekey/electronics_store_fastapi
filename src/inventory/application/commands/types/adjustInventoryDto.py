
class AdjustInventoryDto:
    def __init__(
        self,
        product_id: int,
        stock_change: int,
    ):
        self.productId = product_id
        self.stock = stock_change

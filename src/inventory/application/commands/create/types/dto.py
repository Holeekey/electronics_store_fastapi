from inventory.application.models.inventory import UserRole


class CreateInventoryDto:
    def __init__(
        self,
        product_id: int,
        stock: int,
    ):
        self.productId = product_id
        self.stock = stock

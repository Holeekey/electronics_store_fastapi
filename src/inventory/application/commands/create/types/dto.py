from inventory.application.models.inventory import UserRole


class CreateInventoryDto:
    def __init__(
        self,
        productId: int,
        stock: int,
    ):
        self.productId = productId
        self.stock = stock

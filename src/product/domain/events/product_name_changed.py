from src.common.domain.events.domain_event import DomainEvent

from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_name import ProductName

PRODUCT_NAME_CHANGED = "product_name_changed"


class ProductNameChanged(DomainEvent):
    def __init__(self, product_id: ProductId, name: ProductName):
        super().__init__(PRODUCT_NAME_CHANGED)
        self.product_id = product_id
        self.product_name = name
from src.common.domain.events.domain_event import DomainEvent

from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_code import ProductCode

PRODUCT_CODE_CHANGED = "product_code_changed"


class ProductCodeChanged(DomainEvent):
    def __init__(self, product_id: ProductId, code: ProductCode):
        super().__init__(PRODUCT_CODE_CHANGED)
        self.product_id = product_id
        self.product_code = code
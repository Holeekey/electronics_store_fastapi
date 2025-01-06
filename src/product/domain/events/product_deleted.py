from src.common.domain.events.domain_event import DomainEvent

from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_status import ProductStatusOptions

PRODUCT_DELETED = "product_deleted"


class ProductDeleted(DomainEvent):
    def __init__(self, product_id: ProductId):
        super().__init__(PRODUCT_DELETED)
        self.product_id = product_id
        self.product_status = ProductStatusOptions.INACTIVE
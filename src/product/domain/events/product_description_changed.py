from src.common.domain.events.domain_event import DomainEvent

from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_description import ProductDescription

PRODUCT_DESCRIPTION_CHANGED = "product_description_changed"


class ProductDescriptionChanged(DomainEvent):
    def __init__(self, product_id: ProductId, description: ProductDescription):
        super().__init__(PRODUCT_DESCRIPTION_CHANGED)
        self.product_id = product_id
        self.product_description = description
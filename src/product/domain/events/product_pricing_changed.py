from src.common.domain.events.domain_event import DomainEvent

from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_pricing import ProductPricing

PRODUCT_PRICING_CHANGED = "product_pricing_changed"


class ProductPricingChanged(DomainEvent):
    def __init__(self, product_id: ProductId, pricing: ProductPricing):
        super().__init__(PRODUCT_PRICING_CHANGED)
        self.product_id = product_id
        self.product_pricing = pricing
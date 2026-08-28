from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CheckoutRequest(BaseModel):
    customer_id: UUID
    shipping_address_id: Optional[UUID] = None
    coupon_code: Optional[str] = None


class CheckoutResponse(BaseModel):
    cart_id: UUID
    total_items: int

    subtotal: Decimal
    discount: Decimal
    shipping: Decimal
    tax: Decimal
    grand_total: Decimal

    currency: str

    model_config = ConfigDict(from_attributes=True)
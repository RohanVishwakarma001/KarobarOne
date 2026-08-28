from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CartCouponBase(BaseModel):
    cart_id: UUID
    coupon_id: UUID
    discount_amount: float


class CartCouponCreate(CartCouponBase):
    pass


class CartCouponUpdate(BaseModel):
    discount_amount: float | None = None


class CartCouponResponse(CartCouponBase):
    id: UUID
    applied_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }
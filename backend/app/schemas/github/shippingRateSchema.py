from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ShippingRateCreate(BaseModel):

    shipping_profile_id: UUID
    shipping_zone_id: UUID
    minimum_weight: Decimal
    maximum_weight: Decimal
    shipping_charge: Decimal
    estimated_days_min: int
    estimated_days_max: int


class ShippingRateUpdate(BaseModel):

    minimum_weight: Optional[Decimal] = None
    maximum_weight: Optional[Decimal] = None
    shipping_charge: Optional[Decimal] = None
    estimated_days_min: Optional[int] = None
    estimated_days_max: Optional[int] = None

class ShippingRateResponse(BaseModel):

    id: UUID
    shipping_profile_id: UUID
    shipping_zone_id: UUID
    minimum_weight: Decimal
    maximum_weight: Decimal
    shipping_charge: Decimal
    estimated_days_min: int
    estimated_days_max: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
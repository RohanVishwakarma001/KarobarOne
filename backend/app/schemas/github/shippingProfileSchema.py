from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ShippingProfileCreate(BaseModel):

    tenant_id: UUID

    profile_name: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    description: Optional[str] = None

    free_shipping_threshold: Optional[Decimal] = None

    is_active: bool = True


class ShippingProfileUpdate(BaseModel):

    profile_name: Optional[str] = None

    description: Optional[str] = None

    free_shipping_threshold: Optional[Decimal] = None

    is_active: Optional[bool] = None


class ShippingProfileResponse(BaseModel):

    id: UUID
    tenant_id: UUID
    profile_name: str
    description: Optional[str]
    free_shipping_threshold: Optional[Decimal]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
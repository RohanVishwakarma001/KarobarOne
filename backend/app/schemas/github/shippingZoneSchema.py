from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ShippingZoneCreate(BaseModel):

    tenant_id: UUID

    zone_name: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    zone_code: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    country: str

    state: str

    city: str

    postal_code_pattern: Optional[str] = None

    is_active: bool = True


class ShippingZoneUpdate(BaseModel):

    zone_name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    postal_code_pattern: Optional[str] = None
    is_active: Optional[bool] = None


class ShippingZoneResponse(BaseModel):

    id: UUID
    tenant_id: UUID
    zone_name: str
    zone_code: str
    country: str
    state: str
    city: str
    postal_code_pattern: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
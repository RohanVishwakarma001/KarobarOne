from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ShippingPartnerCreate(BaseModel):
    partner_code: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    partner_name: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    website_url: Optional[HttpUrl] = None

    tracking_url_template: Optional[str] = Field(
        default=None,
        max_length=500
    )

    api_enabled: bool = False
    is_active: bool = True


class ShippingPartnerUpdate(BaseModel):
    partner_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255
    )

    website_url: Optional[HttpUrl] = None

    tracking_url_template: Optional[str] = Field(
        default=None,
        max_length=500
    )

    api_enabled: Optional[bool] = None
    is_active: Optional[bool] = None


class ShippingPartnerResponse(BaseModel):
    id: UUID
    partner_code: str
    partner_name: str
    website_url: Optional[str]
    tracking_url_template: Optional[str]
    api_enabled: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
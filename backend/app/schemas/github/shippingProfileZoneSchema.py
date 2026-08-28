from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ShippingProfileZoneCreate(BaseModel):

    shipping_profile_id: UUID
    shipping_zone_id: UUID


class ShippingProfileZoneResponse(BaseModel):

    id: UUID
    shipping_profile_id: UUID
    shipping_zone_id: UUID
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
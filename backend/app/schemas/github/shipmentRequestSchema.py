from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ShipmentRequestCreate(BaseModel):

    order_id: UUID
    shipping_profile_id: Optional[UUID] = None
    request_status: str = "PENDING"


class ShipmentRequestUpdate(BaseModel):

    request_status: Optional[str] = None


class ShipmentRequestResponse(BaseModel):

    id: UUID
    order_id: UUID
    sshipping_profile_id: Optional[UUID] = None
    request_status: str
    requested_at: datetime
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
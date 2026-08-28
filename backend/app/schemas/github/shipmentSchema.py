from datetime import datetime
from typing import Optional
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ShipmentCreate(BaseModel):

    order_id: UUID

    shipping_partner_id: Optional[UUID] = None

    shipping_partner_id: UUID

    shipment_number: str
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None

    shipment_status: str = "PENDING"


class ShipmentUpdate(BaseModel):

    shipment_number: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipment_status: Optional[str] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


class ShipmentResponse(BaseModel):

    id: UUID
    order_id: UUID
    shipment_request_id: UUID
    shipping_partner_id: UUID
    shipment_number: Optional[str]
    tracking_number: Optional[str]
    tracking_url: Optional[str]
    shipment_status: str
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
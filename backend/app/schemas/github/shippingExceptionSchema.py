from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ShippingExceptionCreate(BaseModel):

    shipment_id: UUID
    exception_type: str
    description: Optional[str] = None


class ShippingExceptionUpdate(BaseModel):

    exception_type: Optional[str] = None
    description: Optional[str] = None
    resolved: Optional[bool] = None
    resolved_at: Optional[datetime] = None


class ShippingExceptionResponse(BaseModel):

    id: UUID
    shipment_id: UUID
    exception_type: str
    description: Optional[str]
    resolved: bool
    resolved_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
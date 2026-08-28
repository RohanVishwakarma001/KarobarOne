from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderCancellationCreate(BaseModel):
    order_id: UUID
    requested_by: Optional[UUID] = None
    cancellation_reason: str
    cancellation_reason_description: Optional[str] = None


class OrderCancellationUpdate(BaseModel):
    status: Optional[str] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    cancellation_reason_description: Optional[str] = None


class OrderCancellationResponse(BaseModel):
    id: UUID
    order_id: UUID
    requested_by: Optional[UUID] = None
    cancellation_reason: str
    cancellation_reason_description: Optional[str] = None
    status: Optional[str] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
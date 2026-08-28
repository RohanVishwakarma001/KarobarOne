from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentReconciliationItemCreate(BaseModel):

    batch_id: UUID
    payment_id: UUID
    gateway_payment_id: Optional[str] = None
    reconciliation_status: str = "MATCHED"
    notes: Optional[str] = None


class PaymentReconciliationItemUpdate(BaseModel):

    reconciliation_status: Optional[str] = None
    notes: Optional[str] = None


class PaymentReconciliationItemResponse(BaseModel):

    id: UUID
    batch_id: UUID
    payment_id: UUID
    gateway_payment_id: Optional[str]
    reconciliation_status: str
    notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
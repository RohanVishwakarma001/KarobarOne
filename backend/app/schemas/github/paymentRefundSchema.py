from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentRefundCreate(BaseModel):

    payment_id: UUID
    refund_amount: Decimal
    refund_reason: Optional[str] = None


class PaymentRefundUpdate(BaseModel):

    refund_reference: Optional[str] = None
    refund_status: Optional[str] = None
    refunded_at: Optional[datetime] = None


class PaymentRefundResponse(BaseModel):

    id: UUID
    payment_id: UUID
    refund_reference: Optional[str]
    refund_amount: Decimal
    refund_reason: Optional[str]
    refund_status: str
    refunded_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
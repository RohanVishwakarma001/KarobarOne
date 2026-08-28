from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubscriptionPaymentCreate(BaseModel):

    tenant_id: UUID
    invoice_id: UUID
    payment_reference: Optional[str] = None
    payment_gateway: str
    subscription_revenue: Decimal
    payment_status: str
    paid_at: Optional[datetime] = None


class SubscriptionPaymentUpdate(BaseModel):

    payment_status: Optional[str] = None
    paid_at: Optional[datetime] = None


class SubscriptionPaymentResponse(BaseModel):

    id: UUID
    tenant_id: UUID
    invoice_id: UUID
    payment_reference: Optional[str]
    payment_gateway: str
    subscription_revenue: Decimal
    payment_status: str
    paid_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
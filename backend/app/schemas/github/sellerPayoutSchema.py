from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SellerPayoutCreate(BaseModel):

    tenant_id: UUID
    payment_id: UUID
    payout_reference: Optional[str] = None
    gross_amount: Decimal
    gateway_fee: Decimal = Decimal("0.00")
    gateway_tax: Decimal = Decimal("0.00")
    platform_commission: Decimal = Decimal("0.00")
    net_payout_amount: Decimal
    payout_status: str = "PENDING"
    payout_date: Optional[datetime] = None


class SellerPayoutUpdate(BaseModel):

    payout_status: Optional[str] = None
    payout_date: Optional[datetime] = None


class SellerPayoutResponse(BaseModel):

    id: UUID
    tenant_id: UUID
    payment_id: UUID
    payout_reference: Optional[str]
    gross_amount: Decimal
    gateway_fee: Decimal
    gateway_tax: Decimal
    platform_commission: Decimal
    net_payout_amount: Decimal
    payout_status: str
    payout_date: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
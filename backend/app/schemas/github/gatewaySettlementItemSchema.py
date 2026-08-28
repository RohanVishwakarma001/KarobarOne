from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GatewaySettlementItemCreate(BaseModel):

    settlement_id: UUID
    payment_id: UUID
    settlement_amount: Decimal
    fee_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")


class GatewaySettlementItemUpdate(BaseModel):

    settlement_amount: Optional[Decimal] = None
    fee_amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None


class GatewaySettlementItemResponse(BaseModel):

    id: UUID
    settlement_id: UUID
    payment_id: UUID
    settlement_amount: Decimal
    fee_amount: Decimal
    tax_amount: Decimal
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
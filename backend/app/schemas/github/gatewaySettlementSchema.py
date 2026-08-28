from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GatewaySettlementCreate(BaseModel):

    settlement_reference: str
    gateway_name: str
    settlement_amount: Decimal
    settlement_date: date
    settlement_status: str = "PENDING"


class GatewaySettlementUpdate(BaseModel):

    settlement_status: Optional[str] = None


class GatewaySettlementResponse(BaseModel):

    id: UUID
    settlement_reference: str
    gateway_name: str
    settlement_amount: Decimal
    settlement_date: date
    settlement_status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
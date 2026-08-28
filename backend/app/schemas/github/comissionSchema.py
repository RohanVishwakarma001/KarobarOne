# Owner: shlokpallav@gmail.com

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommissionRequest(BaseModel):
    order_id: UUID
    order_amount: Decimal = Field(..., gt=0)
    commission_percentage: Decimal = Field(..., ge=0, le=100)


class CommissionResponse(BaseModel):
    order_id: UUID
    order_amount: Decimal
    commission_percentage: Decimal
    commission_amount: Decimal
    seller_amount: Decimal
    message: str

    model_config = ConfigDict(from_attributes=True)
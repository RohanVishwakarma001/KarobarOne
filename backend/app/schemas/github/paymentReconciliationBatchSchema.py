from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentReconciliationBatchCreate(BaseModel):

    batch_number: str
    reconciliation_date: date
    total_payments: int = 0
    total_amount: Decimal = Decimal("0.00")
    status: str = "PENDING"


class PaymentReconciliationBatchUpdate(BaseModel):

    total_payments: Optional[int] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = None


class PaymentReconciliationBatchResponse(BaseModel):

    id: UUID
    batch_number: str
    reconciliation_date: date
    total_payments: int
    total_amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
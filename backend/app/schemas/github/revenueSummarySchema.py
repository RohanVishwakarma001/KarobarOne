from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RevenueSummaryCreate(BaseModel):

    tenant_id: UUID
    report_month: date
    subscription_revenue: Decimal = Decimal("0.00")
    commission_revenue: Decimal = Decimal("0.00")
    total_revenue: Decimal = Decimal("0.00")


class RevenueSummaryUpdate(BaseModel):

   subscription_revenue: Optional[Decimal] = None
   commission_revenue: Optional[Decimal] = None
   total_revenue: Optional[Decimal] = None

class RevenueSummaryResponse(BaseModel):

    id: UUID
    tenant_id: UUID
    report_month: date
    subscription_revenue: Decimal
    commission_revenue: Decimal
    total_revenue: Decimal
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
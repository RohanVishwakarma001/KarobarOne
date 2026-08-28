from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CartCreate(BaseModel):
    tenant_id: UUID
    store_id: UUID
    customer_id: Optional[UUID] = None

    session_id: Optional[str] = Field(
        default=None,
        max_length=255
    )

    cart_status: str = "ACTIVE"

    subtotal_amount: Decimal = Decimal("0.00")
    discount_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    shipping_amount: Decimal = Decimal("0.00")
    total_amount: Decimal = Decimal("0.00")

    currency_code: str = "INR"
    expires_at: Optional[datetime] = None


class CartUpdate(BaseModel):
    cart_status: Optional[str] = None
    subtotal_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    shipping_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    expires_at: Optional[datetime] = None


class CartResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    store_id: UUID
    customer_id: Optional[UUID]
    session_id: Optional[str]

    cart_status: str

    subtotal_amount: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    shipping_amount: Decimal
    total_amount: Decimal

    currency_code: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
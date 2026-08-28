from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):

    tenant_id: UUID
    store_id: UUID
    customer_id: UUID

    cart_id: Optional[UUID] = None

    order_number: str

    payment_id: Optional[UUID] = None

    shipping_profile_id: Optional[UUID] = None

    billing_address_id: UUID

    shipping_address_id: UUID

    order_status: str = "PENDING"

    payment_status: str = "PENDING"

    fulfillment_status: str = "PENDING"

    subtotal_amount: Decimal

    discount_amount: Decimal = Decimal("0.00")

    tax_amount: Decimal = Decimal("0.00")

    shipping_amount: Decimal = Decimal("0.00")

    total_amount: Decimal

    currency_code: str = "INR"

    customer_note: Optional[str] = None


class OrderUpdate(BaseModel):

    order_status: Optional[str] = None

    payment_status: Optional[str] = None

    fulfillment_status: Optional[str] = None

    customer_note: Optional[str] = None


class OrderResponse(BaseModel):

    id: UUID

    tenant_id: UUID

    store_id: UUID

    customer_id: UUID

    cart_id: Optional[UUID]

    order_number: str

    payment_id: Optional[UUID]

    shipping_profile_id: Optional[UUID]

    billing_address_id: UUID

    shipping_address_id: UUID

    order_status: str

    payment_status: str

    fulfillment_status: str

    subtotal_amount: Decimal

    discount_amount: Decimal

    tax_amount: Decimal

    shipping_amount: Decimal

    total_amount: Decimal

    currency_code: str

    customer_note: Optional[str]

    placed_at: datetime

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
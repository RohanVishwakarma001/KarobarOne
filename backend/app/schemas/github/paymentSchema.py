from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):

    tenant_id: UUID
    store_id: UUID
    entity_type: str
    entity_id: UUID
    payment_method_id: UUID
    amount: Decimal
    currency: str = "INR"


class PaymentUpdate(BaseModel):

    payment_status: Optional[str] = None
    payment_reference_number: Optional[str] = None
    payment_date: Optional[datetime] = None


class CreateOrderRequest(BaseModel):

    amount: Decimal
    currency: str = "INR"
    receipt: str


class VerifyPaymentRequest(BaseModel):

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class RefundRequest(BaseModel):

    payment_id: UUID
    amount: Optional[Decimal] = None


class PaymentResponse(BaseModel):

    id: UUID
    tenant_id: UUID
    store_id: UUID
    entity_type: str
    entity_id: UUID
    payment_method_id: UUID
    payment_reference_number: Optional[str]
    amount: Decimal
    currency: str
    payment_status: str
    payment_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
class CreatePaymentOrderRequest(BaseModel):

    tenant_id: UUID
    store_id: UUID
    entity_type: str
    entity_id: UUID
    payment_method_id: UUID
    amount: Decimal
    receipt: str
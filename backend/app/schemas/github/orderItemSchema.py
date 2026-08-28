from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):

    order_id: UUID

    product_id: UUID

    product_variant_id: Optional[UUID] = None

    sku: str

    product_name: str

    variant_name: Optional[str] = None

    hsn_code: Optional[str] = None

    gst_rate: Optional[Decimal] = Decimal("0.00")

    quantity: int

    unit_price: Decimal

    discount_amount: Decimal = Decimal("0.00")

    tax_amount: Decimal = Decimal("0.00")

    shipping_amount: Decimal = Decimal("0.00")

    line_total: Decimal


class OrderItemUpdate(BaseModel):

    quantity: Optional[int] = None

    unit_price: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    tax_amount: Optional[Decimal] = None

    shipping_amount: Optional[Decimal] = None

    line_total: Optional[Decimal] = None


class OrderItemResponse(BaseModel):

    id: UUID

    order_id: UUID

    product_id: UUID

    product_variant_id: Optional[UUID]

    sku: str

    product_name: str

    variant_name: Optional[str]

    hsn_code: Optional[str]

    gst_rate: Optional[Decimal]

    quantity: int

    unit_price: Decimal

    discount_amount: Optional[Decimal]

    tax_amount: Optional[Decimal]

    shipping_amount: Optional[Decimal]

    line_total: Decimal

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
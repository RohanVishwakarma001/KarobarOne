from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):

    tenant_id: UUID
    store_id: UUID
    category_id: UUID

    product_type_id: int

    brand_id: Optional[UUID] = None

    product_name: str = Field(max_length=255)

    product_slug: str = Field(max_length=255)

    short_description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    long_description: Optional[str] = None

    sku_prefix: Optional[str] = Field(
        default=None,
        max_length=50
    )

    quantity_constraint: int = 1

    returnable: bool = False

    cod_available: bool = False

    gst_rate: Decimal = Decimal("0.00")

    hsn_code: Optional[str] = None

    status: str = "DRAFT"

    created_by: UUID


class ProductUpdate(BaseModel):

    product_name: Optional[str] = None

    product_slug: Optional[str] = None

    short_description: Optional[str] = None

    long_description: Optional[str] = None

    quantity_constraint: Optional[int] = None

    returnable: Optional[bool] = None

    cod_available: Optional[bool] = None

    gst_rate: Optional[Decimal] = None

    hsn_code: Optional[str] = None

    status: Optional[str] = None


class ProductResponse(BaseModel):

    id: UUID

    tenant_id: UUID

    store_id: UUID

    category_id: UUID

    product_type_id: int

    brand_id: Optional[UUID]

    product_name: str

    product_slug: str

    short_description: Optional[str]

    long_description: Optional[str]

    status: str

    created_by: UUID

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
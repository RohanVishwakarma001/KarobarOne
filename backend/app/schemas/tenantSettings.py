# Owner: mousamdas156@gmail.com
"""
Pydantic schemas for Tenant Settings.
"""
# Import uuid for validating UUID fields
import uuid
# Import datetime for timestamp fields
from datetime import datetime
# Import Decimal for numeric field representation
from decimal import Decimal
# Import Pydantic base classes for data schemas
from pydantic import BaseModel, Field


class TenantSettingsCreate(BaseModel):
    """
    Schema for validating TenantSettings creation payloads.
    """
    currency: str = Field(default="INR", max_length=10)
    timezone: str = Field(default="Asia/Kolkata", max_length=50)
    language: str = Field(default="en", max_length=10)
    invoicePrefix: str | None = Field(default=None, max_length=50)
    fiscalYearStart: int = Field(default=4, ge=1, le=12)
    taxRate: Decimal = Field(default=Decimal("0.00"), ge=0, le=100)
    enableNotifications: bool = Field(default=True)
    enableAutoRenew: bool = Field(default=True)


class TenantSettingsUpdate(BaseModel):
    """
    Schema for validating TenantSettings partial update/patch payloads.
    """
    currency: str | None = Field(default=None, max_length=10)
    timezone: str | None = Field(default=None, max_length=50)
    language: str | None = Field(default=None, max_length=10)
    invoicePrefix: str | None = Field(default=None, max_length=50)
    fiscalYearStart: int | None = Field(default=None, ge=1, le=12)
    taxRate: Decimal | None = Field(default=None, ge=0, le=100)
    enableNotifications: bool | None = Field(default=None)
    enableAutoRenew: bool | None = Field(default=None)


class TenantSettingsRead(BaseModel):
    """
    Schema representing serialized TenantSettings responses.
    """
    id: uuid.UUID
    tenantId: uuid.UUID
    currency: str
    timezone: str
    language: str
    invoicePrefix: str | None = None
    fiscalYearStart: int
    taxRate: Decimal
    enableNotifications: bool
    enableAutoRenew: bool
    createdAt: datetime
    updatedAt: datetime
    model_config = {"from_attributes": True}

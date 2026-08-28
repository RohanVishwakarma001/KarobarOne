# Owner: mousamdas156@gmail.com
"""
Pydantic schemas for Tenant.
"""

import re
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.domain import DomainRead
from app.schemas.tenantPlan import TenantPlanRead

# Regex patterns matching PostgreSQL CHECK constraints
_PAN_RE = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
_GST_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")
_MOBILE_RE = re.compile(r"^\+[1-9]\d{1,14}$")


class TenantCreate(BaseModel):
    # Basic Information
    gstNumber: str | None = Field(None, max_length=15)
    panNumber: str = Field(..., max_length=10)
    documentMediaLink: str | None = None
    documentVerificationDone: bool = False
    documentVerificationDoneBy: uuid.UUID | None = None
    businessName: str = Field(..., max_length=255)
    legalName: str = Field(..., max_length=255)
    logoMediaId: uuid.UUID | None = None
    email: EmailStr
    mobile: str = Field(..., max_length=15)
    whatsappMobile: str | None = Field(None, max_length=15)
    ownerName: str = Field(..., max_length=150)

    # Address
    businessAddressLine1: str = Field(..., max_length=255)
    businessAddressLine2: str | None = Field(None, max_length=255)
    locationLatitude: Decimal | None = None
    locationLongitude: Decimal | None = None
    landmark: str | None = Field(None, max_length=150)
    postOffice: str | None = Field(None, max_length=100)
    policeStation: str | None = Field(None, max_length=100)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    country: str = Field(default="India", max_length=100)
    postalCode: str = Field(..., max_length=10)

    # Business
    businessType: str = Field(..., max_length=100)
    businessDescription: str | None = None
    employeeCount: int | None = Field(None, ge=0)
    registeredAt: datetime | None = None

    @field_validator("panNumber")
    @classmethod
    def validatePan(cls, v: str) -> str:
        if not _PAN_RE.match(v):
            raise ValueError("PAN must be in format AAAAA9999A (e.g. ABCDE1234F)")
        return v

    @field_validator("gstNumber")
    @classmethod
    def validateGst(cls, v: str | None) -> str | None:
        if v is not None and not _GST_RE.match(v):
            raise ValueError(
                "GST must be 15 chars in GSTIN format "
                "(e.g. 22AAAAA0000A1Z5)"
            )
        return v

    @field_validator("mobile")
    @classmethod
    def validateMobile(cls, v: str) -> str:
        if not _MOBILE_RE.match(v):
            raise ValueError(
                "Mobile must be in E.164 format (e.g. +919876543210)"
            )
        return v


class TenantUpdate(BaseModel):
    gstNumber: str | None = Field(None, max_length=15)
    documentMediaLink: str | None = None
    documentVerificationDone: bool | None = None
    documentVerificationDoneBy: uuid.UUID | None = None
    businessName: str | None = Field(None, max_length=255)
    legalName: str | None = Field(None, max_length=255)
    logoMediaId: uuid.UUID | None = None
    email: EmailStr | None = None
    mobile: str | None = Field(None, max_length=15)
    whatsappMobile: str | None = Field(None, max_length=15)
    ownerName: str | None = Field(None, max_length=150)

    # Address
    businessAddressLine1: str | None = Field(None, max_length=255)
    businessAddressLine2: str | None = Field(None, max_length=255)
    locationLatitude: Decimal | None = None
    locationLongitude: Decimal | None = None
    landmark: str | None = Field(None, max_length=150)
    postOffice: str | None = Field(None, max_length=100)
    policeStation: str | None = Field(None, max_length=100)
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)
    postalCode: str | None = Field(None, max_length=10)

    # Business
    businessType: str | None = Field(None, max_length=100)
    businessDescription: str | None = None
    employeeCount: int | None = Field(None, ge=0)
    statusId: int | None = None
    isActive: bool | None = None


class TenantRead(BaseModel):
    id: uuid.UUID
    gstNumber: str | None = None
    panNumber: str
    documentMediaLink: str | None = None
    documentVerificationDone: bool
    documentVerificationDoneBy: uuid.UUID | None = None
    documentVerificationDoneAt: datetime | None = None
    businessName: str
    legalName: str
    logoMediaId: uuid.UUID | None = None
    email: str
    mobile: str
    whatsappMobile: str | None = None
    ownerName: str

    businessAddressLine1: str
    businessAddressLine2: str | None = None
    locationLatitude: Decimal | None = None
    locationLongitude: Decimal | None = None
    landmark: str | None = None
    postOffice: str | None = None
    policeStation: str | None = None
    city: str
    state: str
    country: str
    postalCode: str

    businessType: str
    businessDescription: str | None = None
    employeeCount: int | None = None
    registeredAt: datetime | None = None

    statusId: int | None = None
    isActive: bool

    planMapping: TenantPlanRead | None = None
    domains: list[DomainRead] = []

    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class TenantRegistrationResponse(BaseModel):
    """
    Returned by POST /tenants. When a regular (non-platform) user registers
    their own business, accessToken/refreshToken carry the freshly-assigned
    STORE_OWNER role + tenantId so the frontend can swap its stored session
    without forcing a re-login. Platform staff creating a tenant on someone
    else's behalf get tenant-only (tokens are null).
    """

    tenant: TenantRead
    accessToken: str | None = None
    refreshToken: str | None = None
    tokenType: str = "bearer"


class TenantReadCompact(BaseModel):
    """Compact tenant response for list endpoints."""

    id: uuid.UUID
    businessName: str
    legalName: str
    email: str
    mobile: str
    city: str
    state: str
    businessType: str
    statusId: int | None = None
    isActive: bool
    createdAt: datetime

    model_config = {"from_attributes": True}

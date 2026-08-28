# Owner - pradhansaikat123@gmail.com
# Pydantic schemas for the Customer API. Uses standard typing, UUID, and IPAddress imports.
# SafeBaseModel ensures incoming timezone-aware datetimes are coerced to naive datetimes to avoid DB mismatches.

from datetime import datetime, timezone  # For date handling and timezone conversions
from typing import Any, Dict, List, Optional, Union  # For Python type annotation support
from uuid import UUID  # For schema UUID fields
from ipaddress import IPv4Address, IPv6Address  # For client IP validations

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator  # Pydantic tools for validation and schemas

from app.core.config import getSettings

settings = getSettings()
DEFAULT_TENANT_ID = UUID(settings.defaultTenantId)
DEFAULT_STORE_ID = UUID(settings.defaultStoreId)


class SafeBaseModel(BaseModel):
    @model_validator(mode="after")
    def make_all_datetimes_naive(self) -> "SafeBaseModel":
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, datetime) and field_value.tzinfo is not None:
                self.__dict__[field_name] = field_value.astimezone(timezone.utc).replace(tzinfo=None)
        return self


# ═══════════════════════════════════════════════
# CUSTOMER SCHEMAS
# ═══════════════════════════════════════════════
class CustomerBase(SafeBaseModel):
    tenantId: UUID = Field(
        default=DEFAULT_TENANT_ID,
        description="Tenant ID",
        examples=["e2e56225-8da9-4414-9d71-d31f368d9ac7"],
    )
    storeId: UUID = Field(
        default=DEFAULT_STORE_ID,
        description="Store ID",
        examples=["d7bb739c-d79d-4ffd-8426-c0378e423f87"],
    )
    customerCode: Optional[str] = Field(
        default=None,
        description="Unique customer code. Auto-generated if omitted.",
        examples=["CUST-1001"],
    )
    firstName: str = Field(..., examples=["John"])
    lastName: Optional[str] = Field(default=None, examples=["Doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    mobile: str = Field(..., examples=["9876543210"])
    status: str = Field(default="ACTIVE", examples=["ACTIVE"])
    isGuestCustomer: bool = Field(default=False, examples=[False])
    isEmailVerified: bool = Field(default=False, examples=[False])
    isMobileVerified: bool = Field(default=False, examples=[False])

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        allowed = {"ACTIVE", "INACTIVE", "BLOCKED"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v


class CustomerCreate(CustomerBase):
    password: Optional[str] = Field(default=None, examples=["password123"])


class CustomerUpdate(SafeBaseModel):
    firstName: Optional[str] = Field(default=None, examples=["John"])
    lastName: Optional[str] = Field(default=None, examples=["Doe"])
    email: Optional[EmailStr] = Field(default=None, examples=["john.doe@example.com"])
    mobile: Optional[str] = Field(default=None, examples=["9876543210"])
    status: Optional[str] = Field(default=None, examples=["ACTIVE"])
    isEmailVerified: Optional[bool] = Field(default=None, examples=[True])
    isMobileVerified: Optional[bool] = Field(default=None, examples=[True])
    isGuestCustomer: Optional[bool] = Field(default=None, examples=[False])

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in {"ACTIVE", "INACTIVE", "BLOCKED"}:
            raise ValueError("status must be ACTIVE, INACTIVE, or BLOCKED")
        return v


class CustomerResponse(CustomerBase):
    id: UUID
    customerCode: str
    lastLoginAt: Optional[datetime] = None
    registeredAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# CUSTOMER ADDRESS SCHEMAS
# ═══════════════════════════════════════════════
class CustomerAddressBase(SafeBaseModel):
    customerId: UUID = Field(..., examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"])
    addressType: str = Field(default="SHIPPING", examples=["SHIPPING"])
    fullName: str = Field(..., examples=["John Doe"])
    mobile: str = Field(..., examples=["9876543210"])
    addressLine1: str = Field(..., examples=["123 Main Street"])
    addressLine2: Optional[str] = Field(default=None, examples=["Suite 4B"])
    landmark: Optional[str] = Field(default=None, examples=["Near City Park"])
    city: str = Field(..., examples=["Mumbai"])
    state: str = Field(..., examples=["Maharashtra"])
    country: str = Field(default="India", examples=["India"])
    postalCode: str = Field(..., examples=["400001"])
    isDefault: bool = Field(default=False, examples=[True])

    @field_validator("addressType")
    @classmethod
    def validate_address_type(cls, v):
        if v not in {"SHIPPING", "BILLING"}:
            raise ValueError("addressType must be SHIPPING or BILLING")
        return v


class CustomerAddressCreate(CustomerAddressBase):
    pass


class CustomerAddressUpdate(SafeBaseModel):
    addressType: Optional[str] = Field(default=None, examples=["SHIPPING"])
    fullName: Optional[str] = Field(default=None, examples=["John Doe"])
    mobile: Optional[str] = Field(default=None, examples=["9876543210"])
    addressLine1: Optional[str] = Field(default=None, examples=["123 Main Street"])
    addressLine2: Optional[str] = Field(default=None, examples=["Suite 4B"])
    landmark: Optional[str] = Field(default=None, examples=["Near City Park"])
    city: Optional[str] = Field(default=None, examples=["Mumbai"])
    state: Optional[str] = Field(default=None, examples=["Maharashtra"])
    country: Optional[str] = Field(default=None, examples=["India"])
    postalCode: Optional[str] = Field(default=None, examples=["400001"])
    isDefault: Optional[bool] = Field(default=None, examples=[True])


class CustomerAddressResponse(CustomerAddressBase):
    id: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# CUSTOMER SESSION SCHEMAS
# ═══════════════════════════════════════════════
class CustomerSessionCreate(SafeBaseModel):
    customerId: UUID = Field(..., examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"])
    refreshTokenHash: str = Field(..., examples=["sample_refresh_token_hash_value"])
    ipAddress: Optional[Union[IPv4Address, IPv6Address, str]] = Field(default="127.0.0.1", examples=["127.0.0.1"])
    userAgent: Optional[str] = Field(default="Mozilla/5.0", examples=["Mozilla/5.0"])
    loginAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expiresAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CustomerSessionUpdate(SafeBaseModel):
    logoutAt: Optional[datetime] = Field(default=None)
    isActive: Optional[bool] = Field(default=None, examples=[False])


class CustomerSessionResponse(CustomerSessionCreate):
    id: UUID
    logoutAt: Optional[datetime] = None
    isActive: bool

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# CUSTOMER ACTIVITY LOG SCHEMAS
# ═══════════════════════════════════════════════
VALID_ACTIVITIES = {
    "LOGIN", "LOGOUT", "ORDER_PLACED", "BOOKING_CREATED",
    "PROFILE_UPDATED", "ADDRESS_ADDED", "WISHLIST_ADDED",
}


class CustomerActivityLogCreate(SafeBaseModel):
    customerId: UUID = Field(..., examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"])
    activityType: str = Field(default="LOGIN", examples=["LOGIN"])
    entityType: Optional[str] = Field(default=None, examples=["CUSTOMER"])
    entityId: Optional[UUID] = Field(default=None)
    activityData: Optional[Dict[str, Any]] = Field(default=None, examples=[{"browser": "Chrome"}])
    ipAddress: Optional[Union[IPv4Address, IPv6Address, str]] = Field(default="127.0.0.1", examples=["127.0.0.1"])

    @field_validator("activityType")
    @classmethod
    def validate_activity(cls, v):
        if v not in VALID_ACTIVITIES:
            raise ValueError(f"activityType must be one of {VALID_ACTIVITIES}")
        return v


class CustomerActivityLogResponse(CustomerActivityLogCreate):
    id: UUID
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# CUSTOMER GROUP SCHEMAS
# ═══════════════════════════════════════════════
class CustomerGroupBase(SafeBaseModel):
    storeId: UUID = Field(
        default=DEFAULT_STORE_ID,
        examples=["d7bb739c-d79d-4ffd-8426-c0378e423f87"],
    )
    groupName: str = Field(..., examples=["VIP Customers"])
    description: Optional[str] = Field(default=None, examples=["High priority customer segment"])


class CustomerGroupCreate(CustomerGroupBase):
    pass


class CustomerGroupUpdate(SafeBaseModel):
    groupName: Optional[str] = Field(default=None, examples=["VIP Customers"])
    description: Optional[str] = Field(default=None, examples=["Updated segment description"])


class CustomerGroupResponse(CustomerGroupBase):
    id: UUID
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# CUSTOMER GROUP MEMBER SCHEMAS
# ═══════════════════════════════════════════════
class CustomerGroupMemberCreate(SafeBaseModel):
    customerId: UUID = Field(..., examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"])
    groupId: UUID = Field(..., examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"])


class CustomerGroupMemberResponse(CustomerGroupMemberCreate):
    id: UUID
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# CUSTOMER NOTE SCHEMAS
# ═══════════════════════════════════════════════
class CustomerNoteCreate(SafeBaseModel):
    customerId: UUID = Field(..., examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"])
    noteText: str = Field(..., examples=["Customer requested priority shipping."])
    createdBy: UUID = Field(..., examples=["e2e56225-8da9-4414-9d71-d31f368d9ac7"])


class CustomerNoteUpdate(SafeBaseModel):
    noteText: str = Field(..., examples=["Updated note content."])


class CustomerNoteResponse(CustomerNoteCreate):
    id: UUID
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# CUSTOMER CONSENT LOG SCHEMAS
# ═══════════════════════════════════════════════



VALID_CONSENTS = {
    "TERMS",
    "PRIVACY_POLICY",
    "COOKIE_POLICY",
    "EMAIL_MARKETING",
    "SMS_MARKETING",
    "WHATSAPP_MARKETING",
}


class CustomerConsentLogCreate(SafeBaseModel):
    customerId: UUID = Field(
        ...,
        examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"],
    )

    consentType: str = Field(
        default="TERMS",
        examples=["TERMS"],
    )

    accepted: bool = Field(
        default=True,
        examples=[True],
    )

    ipAddress: Optional[Union[IPv4Address, IPv6Address, str]] = Field(
        default="127.0.0.1",
        examples=["127.0.0.1"],
    )

    acceptedAt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @field_validator("consentType")
    @classmethod
    def validate_consent(cls, v):
        if v not in VALID_CONSENTS:
            raise ValueError(
                f"consentType must be one of {VALID_CONSENTS}"
            )
        return v


class CustomerConsentLogResponse(CustomerConsentLogCreate):
    id: UUID

    model_config = {
        "from_attributes": True
    }

# ═══════════════════════════════════════════════
# PASSWORD RESET TOKEN SCHEMAS
# ═══════════════════════════════════════════════
class PasswordResetTokenCreate(SafeBaseModel):
    customerId: UUID = Field(..., examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"])
    tokenHash: str = Field(..., examples=["sample_token_hash"])
    expiresAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PasswordResetTokenResponse(PasswordResetTokenCreate):
    id: UUID
    usedAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# GUEST CHECKOUT LOG SCHEMAS
# ═══════════════════════════════════════════════
class GuestCheckoutLogCreate(SafeBaseModel):
    tenantId: UUID = Field(
        default=DEFAULT_TENANT_ID,
        examples=["e2e56225-8da9-4414-9d71-d31f368d9ac7"],
    )
    storeId: UUID = Field(
        default=DEFAULT_STORE_ID,
        examples=["d7bb739c-d79d-4ffd-8426-c0378e423f87"],
    )
    customerId: Optional[UUID] = Field(default=None)
    orderId: Optional[UUID] = Field(default=None)
    bookingId: Optional[UUID] = Field(default=None)
    guestName: str = Field(..., examples=["Jane Guest"])
    guestEmail: EmailStr = Field(..., examples=["jane.guest@example.com"])
    guestMobile: str = Field(..., examples=["9876543210"])
    guestAddressJson: Optional[Dict[str, Any]] = Field(default=None, examples=[{"city": "Mumbai"}])


class GuestCheckoutLogUpdate(SafeBaseModel):
    customerId: Optional[UUID] = Field(default=None)
    convertedToCustomer: Optional[bool] = Field(default=None, examples=[True])
    convertedAt: Optional[datetime] = Field(default=None)


class GuestCheckoutLogResponse(GuestCheckoutLogCreate):
    id: UUID
    convertedToCustomer: bool
    convertedAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# ENTITY VERIFICATION SCHEMAS
# ═══════════════════════════════════════════════
class EntityVerificationCreate(SafeBaseModel):
    entityType: str = Field(default="CUSTOMER", examples=["CUSTOMER"])
    entityId: UUID = Field(..., examples=["3f74287a-a81d-4c7a-89fb-097371e4bbc6"])
    verificationType: str = Field(default="EMAIL", examples=["EMAIL"])
    otpHash: str = Field(..., examples=["sample_otp_hash"])
    expiresAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("entityType")
    @classmethod
    def validate_entity_type(cls, v):
        if v not in {"CUSTOMER", "ORDER", "BOOKING"}:
            raise ValueError("entityType must be CUSTOMER, ORDER, or BOOKING")
        return v

    @field_validator("verificationType")
    @classmethod
    def validate_verification_type(cls, v):
        allowed = {"EMAIL", "MOBILE", "ORDER_CONFIRMATION", "BOOKING_CONFIRMATION"}
        if v not in allowed:
            raise ValueError(f"verificationType must be one of {allowed}")
        return v


class EntityVerificationUpdate(SafeBaseModel):
    verifiedAt: Optional[datetime] = Field(default=None)
    attempts: Optional[int] = Field(default=None, examples=[1])


class EntityVerificationResponse(EntityVerificationCreate):
    id: UUID
    verifiedAt: Optional[datetime] = None
    attempts: int
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# COMMON RESPONSE WRAPPERS
# ═══════════════════════════════════════════════
class PaginatedResponse(SafeBaseModel):
    total: int
    page: int
    pageSize: int
    data: List[Any]

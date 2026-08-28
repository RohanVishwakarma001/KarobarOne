# Owner - pradhansaikat123@gmail.com

import re
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class CustomerBase(BaseModel):
    tenantId: UUID = Field(..., description="The ID of the tenant owning the customer")
    storeId: UUID = Field(..., description="The ID of the store owning the customer")
    firstName: str = Field(..., description="First name of the customer")
    lastName: Optional[str] = Field(None, description="Last name of the customer")
    email: str = Field(..., description="Email address of the customer")
    mobile: str = Field(..., description="Mobile phone number of the customer")

    @field_validator("firstName")
    @classmethod
    def validate_first_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("First name cannot be empty or only spaces")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v.strip().lower()

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        mobile_regex = r"^\+?\d{10,15}$"
        if not re.match(mobile_regex, v):
            raise ValueError("Mobile number must be between 10 and 15 digits (optional leading +)")
        return v.strip()


class CustomerCreate(CustomerBase):
    password: Optional[str] = Field(None, description="Optional password for profile registration")


class CustomerUpdate(BaseModel):
    firstName: Optional[str] = Field(None, description="Updated first name")
    lastName: Optional[str] = Field(None, description="Updated last name")
    email: Optional[str] = Field(None, description="Updated email address")
    mobile: Optional[str] = Field(None, description="Updated mobile phone number")
    status: Optional[str] = Field(None, description="Status of the customer (ACTIVE, INACTIVE, BLOCKED)")

    @field_validator("firstName")
    @classmethod
    def validate_first_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v or not v.strip():
                raise ValueError("First name cannot be empty")
            return v.strip()
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            email_regex = r"^[^@]+@[^@]+\.[^@]+$"
            if not re.match(email_regex, v):
                raise ValueError("Invalid email format")
            return v.strip().lower()
        return v

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            mobile_regex = r"^\+?\d{10,15}$"
            if not re.match(mobile_regex, v):
                raise ValueError("Mobile number must be between 10 and 15 digits (optional leading +)")
            return v.strip()
        return v


class CustomerResponse(BaseModel):
    id: UUID
    tenantId: UUID
    storeId: UUID
    customerCode: str
    firstName: str
    lastName: Optional[str]
    email: str
    mobile: str
    status: str
    isGuestCustomer: bool
    profileImage: Optional[str]
    isEmailVerified: bool
    isMobileVerified: bool
    createdAt: datetime
    updatedAt: datetime
    isActive: bool

    model_config = {"from_attributes": True}


class AddressBase(BaseModel):
    addressType: str = Field(..., description="Type of address: SHIPPING or BILLING")
    fullName: str = Field(..., description="Recipient full name")
    mobile: str = Field(..., description="Contact phone number")
    addressLine1: str = Field(..., description="Street/building address details")
    addressLine2: Optional[str] = Field(None, description="Apartment, suite, unit details")
    landmark: Optional[str] = Field(None, description="Nearby landmark")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State/Province")
    country: Optional[str] = Field("India", description="Country")
    postalCode: str = Field(..., description="Postal or Zip Code")
    isDefault: Optional[bool] = Field(False, description="Set as default billing/shipping address")

    @field_validator("addressType")
    @classmethod
    def validate_address_type(cls, v: str) -> str:
        upper_v = v.strip().upper()
        if upper_v not in ("SHIPPING", "BILLING"):
            raise ValueError("addressType must be SHIPPING or BILLING")
        return upper_v

    @field_validator("fullName", "addressLine1", "city", "state", "postalCode")
    @classmethod
    def validate_required_strings(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        mobile_regex = r"^\+?\d{10,15}$"
        if not re.match(mobile_regex, v):
            raise ValueError("Mobile number must be between 10 and 15 digits")
        return v.strip()


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    addressType: Optional[str] = Field(None)
    fullName: Optional[str] = Field(None)
    mobile: Optional[str] = Field(None)
    addressLine1: Optional[str] = Field(None)
    addressLine2: Optional[str] = Field(None)
    landmark: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    state: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    postalCode: Optional[str] = Field(None)
    isDefault: Optional[bool] = Field(None)

    @field_validator("addressType")
    @classmethod
    def validate_address_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            upper_v = v.strip().upper()
            if upper_v not in ("SHIPPING", "BILLING"):
                raise ValueError("addressType must be SHIPPING or BILLING")
            return upper_v
        return v


class AddressResponse(BaseModel):
    id: UUID
    customerId: UUID
    addressType: str
    fullName: str
    mobile: str
    addressLine1: str
    addressLine2: Optional[str]
    landmark: Optional[str]
    city: str
    state: str
    country: str
    postalCode: str
    isDefault: bool
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class GuestCheckoutRequest(BaseModel):
    tenantId: UUID
    storeId: UUID
    firstName: str
    lastName: Optional[str] = None
    email: str
    mobile: str
    address: Optional[AddressCreate] = None
    totalAmount: Decimal = Field(..., gt=0)

    @field_validator("firstName")
    @classmethod
    def validate_first_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("First name cannot be empty")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v.strip().lower()

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        mobile_regex = r"^\+?\d{10,15}$"
        if not re.match(mobile_regex, v):
            raise ValueError("Mobile number must be between 10 and 15 digits")
        return v.strip()


class CustomerOrderResponse(BaseModel):
    id: UUID
    tenantId: UUID
    storeId: UUID
    customerId: UUID
    orderNumber: str
    totalAmount: Decimal
    status: str
    createdAt: datetime

    model_config = {"from_attributes": True}


class GuestCheckoutResponse(BaseModel):
    message: str
    customer: CustomerResponse
    order: CustomerOrderResponse


class AccountActivationRequest(BaseModel):
    password: str = Field(..., min_length=6, description="Password to enable direct login")


class ProfileImageUploadResponse(BaseModel):
    message: str
    profileImage: str

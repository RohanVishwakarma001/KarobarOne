# Owner - pradhansaikat123@gmail.com
# Pydantic schemas for the Brands and Brand Approvals API.
# Coerces all inbound timezone-aware datetimes to naive datetimes for database compatibility.

# Import regular expressions module for pattern-based validations (URLs, phone numbers, GSTIN)
import re
# Import date, datetime, and timezone for temporal fields and timezone normalization
from datetime import date, datetime, timezone
# Import Any and Optional for type annotations and optional fields
from typing import Any, Optional
# Import UUID class for validated database and object keys
from uuid import UUID
# Import Pydantic base model, configuration tools, and validators for request/response serialization
from pydantic import BaseModel, Field, field_validator, model_validator
# Import email validator function and validation exceptions
from email_validator import validate_email, EmailNotValidError

# Regular expression patterns for validations
URL_REGEX = re.compile(
    r"^(https?:\/\/)?"  # http:// or https:// (optional)
    r"((([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,63})|"  # domain name
    r"localhost|"  # localhost
    r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))"  # ip address
    r"(:\d+)?"  # port (optional)
    r"(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?$"  # path (optional)
)
MOBILE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")
GST_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")


class SafeBaseModel(BaseModel):
    @model_validator(mode="after")
    def makeAllDatetimesNaive(self) -> "SafeBaseModel":
        for fieldName, fieldValue in self.__dict__.items():
            if isinstance(fieldValue, datetime) and fieldValue.tzinfo is not None:
                self.__dict__[fieldName] = fieldValue.astimezone(timezone.utc).replace(tzinfo=None)
        return self


# ═══════════════════════════════════════════════
# BRAND SCHEMAS
# ═══════════════════════════════════════════════
class BrandBase(SafeBaseModel):
    tenantId: Optional[UUID] = Field(default=None, description="Tenant ID referencing tenant details (null for platform brands)")
    ownerStoreId: Optional[UUID] = Field(default=None, description="Store ID owning the brand")
    brandName: str = Field(..., max_length=150, description="Name of the brand")
    brandSlug: Optional[str] = Field(default=None, max_length=180, description="URL-friendly unique slug. If not provided, it will be generated.")
    logoMediaId: Optional[UUID] = Field(default=None, description="Logo media file ID")
    websiteUrl: Optional[str] = Field(default=None, max_length=500, description="Website URL")
    supportEmail: Optional[str] = Field(default=None, max_length=255, description="Support contact email")
    supportMobile: Optional[str] = Field(default=None, max_length=15, description="Support mobile phone in E.164 format")
    description: Optional[str] = Field(default=None, description="General description of the brand")
    countryOfOrigin: Optional[str] = Field(default=None, max_length=100, description="Country of origin")
    gstNumber: Optional[str] = Field(default=None, max_length=15, description="GSTIN number")
    trademarkNumber: Optional[str] = Field(default=None, max_length=100, description="Trademark registration number")
    trademarkDocumentMediaId: Optional[UUID] = Field(default=None, description="Trademark document media file ID")
    verificationStatus: str = Field(default="PENDING", description="Verification status of the brand: PENDING, APPROVED, REJECTED")
    isPlatformBrand: bool = Field(default=False, description="Is this a global platform-managed brand")
    isActive: bool = Field(default=True, description="Indicates if the brand is active")
    createdBy: UUID = Field(..., description="ID of the user who created this brand")

    @field_validator("verificationStatus")
    @classmethod
    def validateVerificationStatus(cls, v):
        if v not in {"PENDING", "APPROVED", "REJECTED"}:
            raise ValueError("verificationStatus must be PENDING, APPROVED, or REJECTED")
        return v

    @field_validator("websiteUrl")
    @classmethod
    def validateWebsiteUrl(cls, v):
        if v is not None and v != "":
            if not URL_REGEX.match(v):
                raise ValueError("Invalid website URL format")
        return v

    @field_validator("supportEmail")
    @classmethod
    def validateSupportEmail(cls, v):
        if v is not None and v != "":
            try:
                validate_email(v, check_deliverability=False)
            except EmailNotValidError as e:
                raise ValueError(f"Invalid support email format: {str(e)}")
        return v

    @field_validator("supportMobile")
    @classmethod
    def validateSupportMobile(cls, v):
        if v is not None and v != "":
            if not MOBILE_REGEX.match(v):
                raise ValueError("Invalid support mobile format. Must match E.164 (e.g. +1234567890)")
        return v

    @field_validator("gstNumber")
    @classmethod
    def validateGstNumber(cls, v):
        if v is not None and v != "":
            if not GST_REGEX.match(v):
                raise ValueError("Invalid GST number format. Must be a valid 15-character GSTIN")
        return v


class BrandCreate(BrandBase):
    pass


class BrandUpdate(SafeBaseModel):
    tenantId: Optional[UUID] = None
    ownerStoreId: Optional[UUID] = None
    brandName: Optional[str] = Field(default=None, max_length=150)
    brandSlug: Optional[str] = Field(default=None, max_length=180)
    logoMediaId: Optional[UUID] = None
    websiteUrl: Optional[str] = Field(default=None, max_length=500)
    supportEmail: Optional[str] = Field(default=None, max_length=255)
    supportMobile: Optional[str] = Field(default=None, max_length=15)
    description: Optional[str] = None
    countryOfOrigin: Optional[str] = Field(default=None, max_length=100)
    gstNumber: Optional[str] = Field(default=None, max_length=15)
    trademarkNumber: Optional[str] = Field(default=None, max_length=100)
    trademarkDocumentMediaId: Optional[UUID] = None
    verificationStatus: Optional[str] = None
    isPlatformBrand: Optional[bool] = None
    isActive: Optional[bool] = None
    approvedBy: Optional[UUID] = None

    @field_validator("verificationStatus")
    @classmethod
    def validateVerificationStatus(cls, v):
        if v is not None:
            if v not in {"PENDING", "APPROVED", "REJECTED"}:
                raise ValueError("verificationStatus must be PENDING, APPROVED, or REJECTED")
        return v

    @field_validator("websiteUrl")
    @classmethod
    def validateWebsiteUrl(cls, v):
        if v is not None and v != "":
            if not URL_REGEX.match(v):
                raise ValueError("Invalid website URL format")
        return v

    @field_validator("supportEmail")
    @classmethod
    def validateSupportEmail(cls, v):
        if v is not None and v != "":
            try:
                validate_email(v, check_deliverability=False)
            except EmailNotValidError as e:
                raise ValueError(f"Invalid support email format: {str(e)}")
        return v

    @field_validator("supportMobile")
    @classmethod
    def validateSupportMobile(cls, v):
        if v is not None and v != "":
            if not MOBILE_REGEX.match(v):
                raise ValueError("Invalid support mobile format. Must match E.164 (e.g. +1234567890)")
        return v

    @field_validator("gstNumber")
    @classmethod
    def validateGstNumber(cls, v):
        if v is not None and v != "":
            if not GST_REGEX.match(v):
                raise ValueError("Invalid GST number format. Must be a valid 15-character GSTIN")
        return v


class BrandResponse(BrandBase):
    id: UUID
    brandSlug: str
    approvedBy: Optional[UUID] = None
    approvedAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# BRAND APPROVAL SCHEMAS
# ═══════════════════════════════════════════════
class BrandApprovalBase(SafeBaseModel):
    brandId: UUID = Field(..., description="ID of the brand being approved")
    requestingStoreId: UUID = Field(..., description="ID of the store requesting approval")
    brandOwnerStoreId: UUID = Field(..., description="ID of the store owning the brand")
    requestStatus: str = Field(default="PENDING", description="Status of the request: PENDING, APPROVED, REJECTED, REVOKED, EXPIRED")
    requestMessage: Optional[str] = Field(default=None, max_length=1000, description="Message from requesting seller")
    supportingDocumentMediaId: Optional[UUID] = Field(default=None, description="ID of authorization/distributorship proof document")
    approvalStartDate: Optional[date] = Field(default=None, description="Start date of approval")
    approvalEndDate: Optional[date] = Field(default=None, description="Optional expiry date of approval")

    @field_validator("requestStatus")
    @classmethod
    def validate_request_status(cls, v):
        if v not in {"PENDING", "APPROVED", "REJECTED", "REVOKED", "EXPIRED"}:
            raise ValueError("requestStatus must be one of: PENDING, APPROVED, REJECTED, REVOKED, EXPIRED")
        return v

    @model_validator(mode="after")
    def validateApprovalConstraints(self) -> "BrandApprovalBase":
        if self.requestingStoreId == self.brandOwnerStoreId:
            raise ValueError("requestingStoreId cannot be the same as brandOwnerStoreId")
        if self.approvalStartDate is not None and self.approvalEndDate is not None:
            if self.approvalStartDate > self.approvalEndDate:
                raise ValueError("approvalStartDate must be less than or equal to approvalEndDate")
        return self


class BrandApprovalCreate(BrandApprovalBase):
    pass


class BrandApprovalUpdate(SafeBaseModel):
    requestStatus: Optional[str] = None
    requestMessage: Optional[str] = Field(default=None, max_length=1000)
    supportingDocumentMediaId: Optional[UUID] = None
    reviewedBy: Optional[UUID] = None
    rejectionReason: Optional[str] = Field(default=None, max_length=1000)
    approvalStartDate: Optional[date] = None
    approvalEndDate: Optional[date] = None
    revokedAt: Optional[datetime] = None
    revokedBy: Optional[UUID] = None

    @field_validator("requestStatus")
    @classmethod
    def validate_request_status(cls, v):
        if v is not None:
            if v not in {"PENDING", "APPROVED", "REJECTED", "REVOKED", "EXPIRED"}:
                raise ValueError("requestStatus must be one of: PENDING, APPROVED, REJECTED, REVOKED, EXPIRED")
        return v

    @model_validator(mode="after")
    def validateUpdateConstraints(self) -> "BrandApprovalUpdate":
        if self.approvalStartDate is not None and self.approvalEndDate is not None:
            if self.approvalStartDate > self.approvalEndDate:
                raise ValueError("approvalStartDate must be less than or equal to approvalEndDate")
        return self


class BrandApprovalResponse(BrandApprovalBase):
    id: UUID
    reviewedBy: Optional[UUID] = None
    reviewedAt: Optional[datetime] = None
    rejectionReason: Optional[str] = None
    revokedAt: Optional[datetime] = None
    revokedBy: Optional[UUID] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

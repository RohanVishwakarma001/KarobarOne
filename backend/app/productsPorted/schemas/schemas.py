# Owner - pradhansaikat123@gmail.com

# Pydantic schemas for Categories, Products, Variants, Attributes, 
# Product Images, Shipping Profiles, and Brand Approval workflow.

# Import datetime and timezone from datetime for datetime validations
from datetime import datetime, timezone
# Import Any, Dict, List, Optional from typing for schema field types
from typing import Any, Dict, List, Optional
# Import UUID from uuid for unique identifiers in schemas
from uuid import UUID

# Import BaseModel, Field, field_validator, model_validator from pydantic for schema validations
from pydantic import BaseModel, Field, field_validator, model_validator


class SafeBaseModel(BaseModel):
    @model_validator(mode="after")
    def make_all_datetimes_naive(self) -> "SafeBaseModel":
        for fieldName, fieldValue in self.__dict__.items():
            if isinstance(fieldValue, datetime) and fieldValue.tzinfo is not None:
                self.__dict__[fieldName] = fieldValue.astimezone(timezone.utc).replace(tzinfo=None)
        return self


# ─────────────────────────────────────────────
# CATEGORY SCHEMAS
# ─────────────────────────────────────────────
class CategoryBase(SafeBaseModel):
    tenantId: UUID
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    parentId: Optional[UUID] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SafeBaseModel):
    name: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=100)
    parentId: Optional[UUID] = None


class CategoryResponse(CategoryBase):
    id: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# SHIPPING PROFILE SCHEMAS
# ─────────────────────────────────────────────
class ShippingProfileBase(SafeBaseModel):
    tenantId: UUID
    name: str = Field(..., max_length=100)
    deliveryEstimate: str = Field(..., max_length=100)
    charges: float = Field(default=0.0, ge=0.0)


class ShippingProfileCreate(ShippingProfileBase):
    pass


class ShippingProfileUpdate(SafeBaseModel):
    name: Optional[str] = Field(None, max_length=100)
    deliveryEstimate: Optional[str] = Field(None, max_length=100)
    charges: Optional[float] = Field(None, ge=0.0)


class ShippingProfileResponse(ShippingProfileBase):
    id: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── BRAND SCHEMAS ────────────────────────────
class BrandBase(SafeBaseModel):
    tenantId: UUID
    name: str = Field(..., max_length=100)
    logoUrl: Optional[str] = Field(None, max_length=255)


class BrandCreate(BrandBase):
    pass


class BrandUpdate(SafeBaseModel):
    name: Optional[str] = Field(None, max_length=100)
    logoUrl: Optional[str] = Field(None, max_length=255)


class BrandResponse(BrandBase):
    id: UUID
    isApproved: bool
    approvedBy: Optional[UUID] = None
    approvedAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── BRAND APPROVAL SCHEMAS ───────────────────
class BrandApprovalRequestCreate(SafeBaseModel):
    brandId: UUID
    requestedBy: UUID


class BrandApprovalDecision(SafeBaseModel):
    performedBy: UUID
    notes: Optional[str] = None
    rejectionReason: Optional[str] = None


class BrandApprovalRequestResponse(SafeBaseModel):
    id: UUID
    brandId: UUID
    requestedBy: UUID
    status: str
    rejectionReason: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BrandApprovalAuditLogResponse(SafeBaseModel):
    id: UUID
    brandId: UUID
    requestId: UUID
    action: str
    performedBy: UUID
    notes: Optional[str] = None
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── ATTRIBUTE SCHEMAS ────────────────────────
class AttributeBase(SafeBaseModel):
    tenantId: UUID
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=100)
    type: str = Field(default="text", max_length=50)  # text, select, multi-select, boolean

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        allowed = {"text", "select", "multi-select", "boolean"}
        if v not in allowed:
            raise ValueError(f"type must be one of {allowed}")
        return v


class AttributeCreate(AttributeBase):
    pass


class AttributeUpdate(SafeBaseModel):
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=100)
    type: Optional[str] = Field(None, max_length=50)

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v is not None:
            allowed = {"text", "select", "multi-select", "boolean"}
            if v not in allowed:
                raise ValueError(f"type must be one of {allowed}")
        return v


class AttributeResponse(AttributeBase):
    id: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── PRODUCT ATTRIBUTE MAPPING SCHEMAS ─────────
class ProductAttributeMappingBase(SafeBaseModel):
    attributeId: UUID
    value: str = Field(..., max_length=255)


class ProductAttributeMappingCreate(ProductAttributeMappingBase):
    pass


class ProductAttributeMappingResponse(ProductAttributeMappingBase):
    id: UUID
    productId: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── VARIANT SCHEMAS ──────────────────────────
class VariantBase(SafeBaseModel):
    sku: str = Field(..., max_length=100)
    price: float = Field(..., ge=0.0)
    inventory: int = Field(default=0, ge=0)
    attributes: Optional[Dict[str, Any]] = None  # e.g., {"color": "Red", "size": "L"}


class VariantCreate(VariantBase):
    productId: UUID


class VariantUpdate(SafeBaseModel):
    sku: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, ge=0.0)
    inventory: Optional[int] = Field(None, ge=0)
    attributes: Optional[Dict[str, Any]] = None


class VariantResponse(VariantBase):
    id: UUID
    productId: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── PRODUCT IMAGE SCHEMAS ────────────────────
class ProductImageBase(SafeBaseModel):
    url: str = Field(..., max_length=255)
    altText: Optional[str] = Field(None, max_length=255)
    isPrimary: bool = False
    fileSize: int = Field(..., ge=0)
    fileType: str = Field(..., max_length=100)


class ProductImageCreate(ProductImageBase):
    productId: UUID


class ProductImageResponse(ProductImageBase):
    id: UUID
    productId: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── PRODUCT SCHEMAS ──────────────────────────
class ProductBase(SafeBaseModel):
    tenantId: UUID
    storeId: UUID
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="DRAFT")  # DRAFT, PENDING, PUBLISHED, ARCHIVED
    productType: str = Field(default="PHYSICAL")  # PHYSICAL, DIGITAL
    sku: Optional[str] = Field(None, max_length=100)
    metaTitle: Optional[str] = Field(None, max_length=255)
    metaDescription: Optional[str] = None
    categoryId: Optional[UUID] = None
    brandId: Optional[UUID] = None
    shippingProfileId: Optional[UUID] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty or blank whitespace")
        return v.strip()

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if not v or not v.strip():
            raise ValueError("Product slug cannot be empty or blank whitespace")
        return v.strip()

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        allowed = {"DRAFT", "PENDING", "PUBLISHED", "ARCHIVED", "ACTIVE"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v

    @field_validator("productType")
    @classmethod
    def validate_product_type(cls, v):
        allowed = {"PHYSICAL", "DIGITAL"}
        if v not in allowed:
            raise ValueError(f"productType must be one of {allowed}")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SafeBaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    productType: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)
    metaTitle: Optional[str] = Field(None, max_length=255)
    metaDescription: Optional[str] = None
    categoryId: Optional[UUID] = None
    brandId: Optional[UUID] = None
    shippingProfileId: Optional[UUID] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Product name cannot be empty or blank whitespace")
            return v.strip()
        return v

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Product slug cannot be empty or blank whitespace")
            return v.strip()
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            allowed = {"DRAFT", "PENDING", "PUBLISHED", "ARCHIVED", "ACTIVE"}
            if v not in allowed:
                raise ValueError(f"status must be one of {allowed}")
        return v

    @field_validator("productType")
    @classmethod
    def validate_product_type(cls, v):
        if v is not None:
            allowed = {"PHYSICAL", "DIGITAL"}
            if v not in allowed:
                raise ValueError(f"productType must be one of {allowed}")
        return v


class ProductResponse(ProductBase):
    id: UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    # Nested relations
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None
    shippingProfile: Optional[ShippingProfileResponse] = None
    variants: List[VariantResponse] = []
    images: List[ProductImageResponse] = []
    attributeMappings: List[ProductAttributeMappingResponse] = []

    model_config = {"from_attributes": True}


# ── PAGINATED RESPONSE SCHEMAS ───────────────
class PaginatedResponse(SafeBaseModel):
    total: int
    page: int
    pageSize: int
    data: List[Any]


class ProductPaginatedResponse(SafeBaseModel):
    total: int
    page: int
    pageSize: int
    data: List[ProductResponse]


# ── BULK IMPORT SCHEMAS ──────────────────────
class BulkRowError(SafeBaseModel):
    row: int
    data: Dict[str, Any]
    errors: List[str]


class BulkImportResponse(SafeBaseModel):
    totalRows: int
    successfulCount: int
    failedCount: int
    createdProducts: List[ProductResponse]
    rowErrors: List[BulkRowError]

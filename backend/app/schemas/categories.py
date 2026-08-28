# Owner - pradhansaikat123@gmail.com
# Pydantic schemas for the Category API. Uses standard typing and UUID imports.
# SafeBaseModel ensures incoming timezone-aware datetimes are coerced to naive datetimes to avoid DB mismatches.

from datetime import datetime, timezone  # Datetime and timezone utilities
from typing import Any, List, Optional  # Type annotations and hints
from uuid import UUID  # Universally Unique Identifier type

from pydantic import BaseModel, Field, field_validator, model_validator  # Pydantic validation and field customization

from app.core.config import getSettings

settings = getSettings()
defaultTenantId = UUID(settings.defaultTenantId)
defaultStoreId = UUID(settings.defaultStoreId)


class SafeBaseModel(BaseModel):
    @model_validator(mode="after")
    def make_all_datetimes_naive(self) -> "SafeBaseModel":
        for fieldName, fieldValue in self.__dict__.items():
            if isinstance(fieldValue, datetime) and fieldValue.tzinfo is not None:
                self.__dict__[fieldName] = fieldValue.astimezone(timezone.utc).replace(tzinfo=None)
        return self


# ═══════════════════════════════════════════════
# CATEGORY SCHEMAS
# ═══════════════════════════════════════════════
class CategoryBase(SafeBaseModel):
    tenantId: Optional[UUID] = Field(
        default=defaultTenantId,
        description="Tenant ID. Null for system categories.",
        examples=["e2e56225-8da9-4414-9d71-d31f368d9ac7"],
    )
    storeId: Optional[UUID] = Field(
        default=defaultStoreId,
        description="Store ID. Null for platform categories.",
        examples=["d7bb739c-d79d-4ffd-8426-c0378e423f87"],
    )
    parentCategoryId: Optional[UUID] = Field(
        default=None,
        description="ID of parent category. Supports hierarchy.",
        examples=[None],
    )
    categoryType: str = Field(..., description="PRODUCT / SERVICE / BOTH", examples=["PRODUCT"])
    categoryName: str = Field(..., max_length=150, description="Category name", examples=["Electronics"])
    categorySlug: Optional[str] = Field(default=None, max_length=180, description="URL slug. Auto-generated from name if omitted.", examples=["electronics"])
    shortDescription: Optional[str] = Field(default=None, max_length=500, description="Short summary", examples=["Electronic goods and devices"])
    longDescription: Optional[str] = Field(default=None, description="Detailed category overview", examples=["A long text description of electronics products."])
    imageMediaId: Optional[UUID] = Field(default=None, description="Category image attachment ID", examples=[None])
    iconMediaId: Optional[UUID] = Field(default=None, description="Category icon attachment ID", examples=[None])
    displayOrder: int = Field(default=0, description="Order of category display in lists", examples=[0])
    levelNumber: int = Field(default=1, description="Cached level in hierarchy", examples=[1])
    approvalStatus: str = Field(default="PENDING", description="PENDING / APPROVED / REJECTED", examples=["PENDING"])
    isSystemCategory: bool = Field(default=False, description="Whether platform managed", examples=[False])
    isActive: bool = Field(default=True, description="Active status visibility", examples=[True])
    createdBy: UUID = Field(..., description="ID of the user who created this category", examples=["e2e56225-8da9-4414-9d71-d31f368d9ac7"])

    @field_validator("categoryType")
    @classmethod
    def validate_category_type(cls, v):
        allowed = {"PRODUCT", "SERVICE", "BOTH"}
        if v not in allowed:
            raise ValueError(f"categoryType must be one of {allowed}")
        return v

    @field_validator("approvalStatus")
    @classmethod
    def validate_approval_status(cls, v):
        allowed = {"PENDING", "APPROVED", "REJECTED"}
        if v not in allowed:
            raise ValueError(f"approvalStatus must be one of {allowed}")
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SafeBaseModel):
    tenantId: Optional[UUID] = Field(default=None)
    storeId: Optional[UUID] = Field(default=None)
    parentCategoryId: Optional[UUID] = Field(default=None)
    categoryType: Optional[str] = Field(default=None)
    categoryName: Optional[str] = Field(default=None, max_length=150)
    categorySlug: Optional[str] = Field(default=None, max_length=180)
    shortDescription: Optional[str] = Field(default=None, max_length=500)
    longDescription: Optional[str] = Field(default=None)
    imageMediaId: Optional[UUID] = Field(default=None)
    iconMediaId: Optional[UUID] = Field(default=None)
    displayOrder: Optional[int] = Field(default=None)
    levelNumber: Optional[int] = Field(default=None)
    approvalStatus: Optional[str] = Field(default=None)
    isSystemCategory: Optional[bool] = Field(default=None)
    isActive: Optional[bool] = Field(default=None)
    approvedBy: Optional[UUID] = Field(default=None)
    approvedAt: Optional[datetime] = Field(default=None)

    @field_validator("categoryType")
    @classmethod
    def validate_category_type(cls, v):
        if v is not None and v not in {"PRODUCT", "SERVICE", "BOTH"}:
            raise ValueError("categoryType must be PRODUCT, SERVICE, or BOTH")
        return v

    @field_validator("approvalStatus")
    @classmethod
    def validate_approval_status(cls, v):
        if v is not None and v not in {"PENDING", "APPROVED", "REJECTED"}:
            raise ValueError("approvalStatus must be PENDING, APPROVED, or REJECTED")
        return v


class CategoryResponse(CategoryBase):
    id: UUID
    approvedBy: Optional[UUID] = None
    approvedAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# COMMON RESPONSE WRAPPERS
# ═══════════════════════════════════════════════
class PaginatedResponse(SafeBaseModel):
    total: int
    page: int
    pageSize: int
    data: List[CategoryResponse]

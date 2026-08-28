# Owner - pradhansaikat123@gmail.com
# Pydantic schemas for the Tag API.
# SafeBaseModel ensures incoming timezone-aware datetimes are coerced to naive datetimes to avoid DB mismatches.

import re
from datetime import datetime, timezone
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

from app.core.config import getSettings

settings = getSettings()
DEFAULT_TENANT_ID = UUID(settings.defaultTenantId)
DEFAULT_STORE_ID = UUID(settings.defaultStoreId)
DEFAULT_USER_ID = UUID(settings.defaultUserId)


class SafeBaseModel(BaseModel):
    @model_validator(mode="after")
    def make_all_datetimes_naive(self) -> "SafeBaseModel":
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, datetime) and field_value.tzinfo is not None:
                self.__dict__[field_name] = field_value.astimezone(timezone.utc).replace(tzinfo=None)
        return self


# ═══════════════════════════════════════════════
# TAG SCHEMAS
# ═══════════════════════════════════════════════
class TagBase(SafeBaseModel):
    tenantId: Optional[UUID] = Field(
        default=DEFAULT_TENANT_ID,
        description="Tenant ID. Null for platform tags.",
        examples=["e2e56225-8da9-4414-9d71-d31f368d9ac7"],
    )
    storeId: Optional[UUID] = Field(
        default=DEFAULT_STORE_ID,
        description="Store ID. Null for platform tags.",
        examples=["d7bb739c-d79d-4ffd-8426-c0378e423f87"],
    )
    tagName: str = Field(..., max_length=100, examples=["Summer Sale"])
    tagSlug: Optional[str] = Field(
        default=None,
        max_length=120,
        description="URL-friendly unique identifier. Auto-generated if omitted.",
        examples=["summer-sale"],
    )
    tagType: str = Field(..., examples=["PRODUCT"])
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        examples=["Tag for summer promotional items"],
    )
    colorCode: Optional[str] = Field(default=None, examples=["#FF5733"])
    isSystemTag: bool = Field(default=False)
    isActive: bool = Field(default=True)
    createdBy: UUID = Field(default=DEFAULT_USER_ID)

    @field_validator("tagType")
    @classmethod
    def validate_tag_type(cls, v):
        allowed = {
            "PRODUCT",
            "SERVICE",
            "CUSTOMER",
            "ORDER",
            "BOOKING",
            "BLOG",
            "OFFER",
            "CATEGORY",
            "BRAND",
            "GENERAL",
        }
        if v not in allowed:
            raise ValueError(f"tagType must be one of {allowed}")
        return v

    @field_validator("colorCode")
    @classmethod
    def validate_color_code(cls, v):
        if v is not None:
            if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
                raise ValueError("colorCode must be null or in hex format (e.g. #RRGGBB)")
        return v


class TagCreate(TagBase):
    pass


class TagUpdate(SafeBaseModel):
    tagName: Optional[str] = Field(default=None, max_length=100)
    tagSlug: Optional[str] = Field(default=None, max_length=120)
    tagType: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=500)
    colorCode: Optional[str] = Field(default=None)
    isSystemTag: Optional[bool] = Field(default=None)
    isActive: Optional[bool] = Field(default=None)

    @field_validator("tagType")
    @classmethod
    def validate_tag_type(cls, v):
        if v is not None:
            allowed = {
                "PRODUCT",
                "SERVICE",
                "CUSTOMER",
                "ORDER",
                "BOOKING",
                "BLOG",
                "OFFER",
                "CATEGORY",
                "BRAND",
                "GENERAL",
            }
            if v not in allowed:
                raise ValueError(f"tagType must be one of {allowed}")
        return v

    @field_validator("colorCode")
    @classmethod
    def validate_color_code(cls, v):
        if v is not None:
            if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
                raise ValueError("colorCode must be null or in hex format (e.g. #RRGGBB)")
        return v


class TagResponse(TagBase):
    id: UUID
    createdAt: datetime
    updatedAt: datetime
    deletedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# TAG MAPPING SCHEMAS
# ═══════════════════════════════════════════════
class TagMappingBase(SafeBaseModel):
    tagId: UUID = Field(..., description="The ID of the tag to apply.")
    entityType: str = Field(..., description="Type of entity being tagged.", examples=["PRODUCT"])
    entityId: UUID = Field(..., description="The ID of the entity being tagged.")
    mappedBy: UUID = Field(default=DEFAULT_USER_ID, description="User ID of the mapper.")

    @field_validator("entityType")
    @classmethod
    def validate_entity_type(cls, v):
        allowed = {
            "PRODUCT",
            "SERVICE",
            "CUSTOMER",
            "ORDER",
            "BOOKING",
            "BLOG",
            "OFFER",
            "CATEGORY",
            "BRAND",
        }
        if v not in allowed:
            raise ValueError(f"entityType must be one of {allowed}")
        return v


class TagMappingCreate(TagMappingBase):
    pass


class TagMappingResponse(TagMappingBase):
    id: UUID
    createdAt: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════
# COMMON RESPONSE WRAPPERS
# ═══════════════════════════════════════════════
class PaginatedResponse(SafeBaseModel):
    total: int
    page: int
    pageSize: int
    data: List[Any]

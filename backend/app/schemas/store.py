# Owner: mousamdas156@gmail.com
"""
================================================================================
STORE DATA SCHEMAS
================================================================================
Yeh file dukaano (stores) ke input aur output properties ko validation rules ke sath define karti hai.
This module defines Pydantic schemas for data validation and serialization of Stores.

Why it is used:
- Enforces data integrity checks (like email formats using EmailStr, string length bounds).
================================================================================
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# ── Create Request Schema ──────────────────────────────────────────
class StoreCreate(BaseModel):
    """
    Schema for validating storefront creation inputs.
    """
    # Tenant ID representing the merchant account who owns this store
    tenantId: uuid.UUID
    
    # Store visual name (e.g. "Jack's Boutique")
    storeName: str = Field(..., max_length=150)
    
    # Store URL friendly unique slug (e.g. "jacks-boutique")
    storeSlug: str = Field(..., max_length=100)
    
    # Optional business tagline statement
    tagline: str | None = Field(None, max_length=255)
    
    # Official contact email address (validated using Pydantic EmailStr)
    email: EmailStr | None = Field(None)
    
    # Customer support phone number
    mobile: str | None = Field(None, max_length=15)
    
    # Dedicated WhatsApp support contact mobile
    whatsappMobile: str | None = Field(None, max_length=15)
    
    # Store description text
    description: str | None = None
    
    # Optional image UUID references from media uploads
    logoMediaId: uuid.UUID | None = None
    faviconMediaId: uuid.UUID | None = None
    heroMediaId: uuid.UUID | None = None
    
    # Active publishing status flag
    isActive: bool = True
    
    # Store verification/approval status (DB check constraint only allows PENDING|APPROVED|REJECTED)
    approvalStatus: str = Field("PENDING", max_length=20)


# ── Update Request Schema ──────────────────────────────────────────
class StoreUpdate(BaseModel):
    """
    Schema for validating storefront configuration partial updates.
    """
    storeName: str | None = Field(None, max_length=150)
    storeSlug: str | None = Field(None, max_length=100)
    tagline: str | None = Field(None, max_length=255)
    email: EmailStr | None = Field(None)
    mobile: str | None = Field(None, max_length=15)
    whatsappMobile: str | None = Field(None, max_length=15)
    description: str | None = None
    logoMediaId: uuid.UUID | None = None
    faviconMediaId: uuid.UUID | None = None
    heroMediaId: uuid.UUID | None = None
    isActive: bool | None = None
    approvalStatus: str | None = Field(None, max_length=20)


# ── Response Serialization Schema ────────────────────────────────────
class StoreResponse(BaseModel):
    """
    Schema representing a store configuration profile returned to the API client.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenantId: uuid.UUID
    storeName: str
    storeSlug: str
    tagline: str | None
    email: str | None
    mobile: str | None
    whatsappMobile: str | None
    description: str | None
    logoMediaId: uuid.UUID | None
    faviconMediaId: uuid.UUID | None
    heroMediaId: uuid.UUID | None
    isActive: bool
    approvalStatus: str
    createdAt: datetime
    updatedAt: datetime


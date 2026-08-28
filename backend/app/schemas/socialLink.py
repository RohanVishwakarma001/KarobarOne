# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL LINK DATA SCHEMAS
================================================================================
Yeh file social links map karne ke input aur output schemas ko manage karti hai.
This module defines Pydantic schemas for validation and serialization of SocialLinks.

Why it is used:
- Validates the merchant's profile URL format and length constraints.
================================================================================
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ── Create Request Schema ──────────────────────────────────────────
class SocialLinkCreate(BaseModel):
    """
    Schema for validating social link mapping inputs.
    """
    # Store linking to the social account
    storeId: uuid.UUID
    
    # Master platform being connected
    platformId: uuid.UUID
    
    # Full handle URL (e.g. 'https://facebook.com/store')
    profileUrl: str = Field(..., max_length=255)
    
    # Display toggle status
    isActive: bool = True


# ── Update Request Schema ──────────────────────────────────────────
class SocialLinkUpdate(BaseModel):
    """
    Schema for validating partial updates of store social links.
    """
    profileUrl: str | None = Field(None, max_length=255)
    isActive: bool | None = None


# ── Response Serialization Schema ────────────────────────────────────
class SocialLinkResponse(BaseModel):
    """
    Schema representing a social link returned to the API client.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    storeId: uuid.UUID
    platformId: uuid.UUID
    profileUrl: str
    isActive: bool
    createdAt: datetime

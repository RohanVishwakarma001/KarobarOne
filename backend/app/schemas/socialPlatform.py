# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL PLATFORM DATA SCHEMAS
================================================================================
Yeh file social platforms master table ke input aur output schemas ko manage karti hai.
This module defines Pydantic validation schemas for the SocialPlatform entity.

Why it is used:
- Enforces code standard formats (e.g. 'INSTAGRAM') and constraints on master values.
================================================================================
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ── Create Request Schema ──────────────────────────────────────────
class SocialPlatformCreate(BaseModel):
    """
    Schema for validating master social platform registration inputs.
    """
    # Platform code identifier (e.g. 'TWITTER')
    platformCode: str = Field(..., max_length=50)
    
    # Platform friendly name (e.g. 'Twitter')
    platformName: str = Field(..., max_length=100)
    
    # Base web pattern (e.g. 'https://twitter.com/')
    baseUrl: str | None = Field(None, max_length=255)
    
    # Optional foreign key to logo media icon
    iconMediaId: uuid.UUID | None = None
    
    # Active flag
    isActive: bool = True


# ── Update Request Schema ──────────────────────────────────────────
class SocialPlatformUpdate(BaseModel):
    """
    Schema for validating social platform partial updates.
    """
    platformName: str | None = Field(None, max_length=100)
    baseUrl: str | None = Field(None, max_length=255)
    iconMediaId: uuid.UUID | None = None
    isActive: bool | None = None


# ── Response Serialization Schema ────────────────────────────────────
class SocialPlatformResponse(BaseModel):
    """
    Schema representing a social platform returned to the API client.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    platformCode: str
    platformName: str
    baseUrl: str | None
    iconMediaId: uuid.UUID | None
    isActive: bool
    createdAt: datetime

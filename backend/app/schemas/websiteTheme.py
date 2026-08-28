# Owner: mousamdas156@gmail.com
"""
================================================================================
WEBSITE THEME DATA SCHEMAS
================================================================================
Yeh file website design themes ke input aur output schemas ko manage karti hai.
This module defines Pydantic validation schemas for the WebsiteTheme entity.

Why it is used:
- Validates the design preset properties prior to database creation.
================================================================================
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ── Create Request Schema ──────────────────────────────────────────
class WebsiteThemeCreate(BaseModel):
    """
    Schema for validating website design theme template registration inputs.
    """
    # Design theme name
    themeName: str = Field(..., max_length=100)
    
    # Design theme code string (e.g. 'LIGHT_MODE')
    themeCode: str = Field(..., max_length=50)
    
    # Optional preview media image ID
    previewImageId: uuid.UUID | None = None
    
    # Design theme configuration schema details
    configSchema: dict | list | None = None
    
    # Active status flag
    isActive: bool = True


# ── Update Request Schema ──────────────────────────────────────────
class WebsiteThemeUpdate(BaseModel):
    """
    Schema for validating design theme template partial updates.
    """
    themeName: str | None = Field(None, max_length=100)
    themeCode: str | None = Field(None, max_length=50)
    previewImageId: uuid.UUID | None = None
    configSchema: dict | list | None = None
    isActive: bool | None = None


# ── Response Serialization Schema ────────────────────────────────────
class WebsiteThemeResponse(BaseModel):
    """
    Schema representing a website theme layout returned to the API client.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    themeName: str
    themeCode: str
    previewImageId: uuid.UUID | None
    configSchema: dict | list | None
    isActive: bool
    createdAt: datetime

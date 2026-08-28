# Owner: mousamdas156@gmail.com
"""
================================================================================
SECTION DATA SCHEMAS
================================================================================
Yeh file page sections ke input aur output models (Pydantic validation schemas) ko define karti hai.
This module defines Pydantic schemas for data validation and serialization of Sections.

Why it is used:
- Validates data format and lengths before database entry.
- Defines clear contract structures for HTTP requests and responses.
================================================================================
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ── Create Request Schema ──────────────────────────────────────────
class SectionCreate(BaseModel):
    """
    Schema for validating section creation inputs.
    """
    # UUID of the store this section block belongs to
    storeId: uuid.UUID
    
    # Unique code name of the section block (e.g. 'HERO_BANNER')
    sectionCode: str = Field(..., max_length=50)
    
    # Display label of the section block
    sectionName: str = Field(..., max_length=100)
    
    # Layout type of the section (e.g. 'HERO')
    sectionType: str = Field(..., max_length=50)
    
    # Display ordering sequence index number (greater than or equal to 0)
    sortOrder: int = Field(..., ge=0)
    
    # Active flag (defaults to True)
    isActive: bool = True
    
    # Flex configuration attributes (fonts, links, text)
    configData: dict | list | None = None


# ── Update Request Schema ──────────────────────────────────────────
class SectionUpdate(BaseModel):
    """
    Schema for validating section partial updates.
    Fields are optional so client can specify only modified ones.
    """
    sectionName: str | None = Field(None, max_length=100)
    sectionType: str | None = Field(None, max_length=50)
    sortOrder: int | None = Field(None, ge=0)
    isActive: bool | None = None
    configData: dict | list | None = None


# ── Response Serialization Schema ────────────────────────────────────
class SectionResponse(BaseModel):
    """
    Schema representing a section returned to API client.
    """
    # Instructs Pydantic to read attributes directly from SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    storeId: uuid.UUID
    sectionCode: str
    sectionName: str
    sectionType: str
    sortOrder: int
    isActive: bool
    configData: dict | list | None
    createdAt: datetime
    updatedAt: datetime


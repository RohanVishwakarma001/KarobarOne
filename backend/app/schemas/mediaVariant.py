# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA VARIANT SCHEMAS (mediaVariant.py)
================================================================================
Why this file is used:
- This file contains the Pydantic validation models for creating, updating, and 
  representing `MediaVariant` instances.
- It ensures strict data type checking for resized asset fields.
================================================================================
"""

# Standard library imports for UUIDs and datetime format validations
import uuid
from datetime import datetime

# Third-party Pydantic components for data validation and schema creation
from pydantic import BaseModel, ConfigDict, Field


class MediaVariantCreate(BaseModel):
    """
    Schema for validating input when creating a new MediaVariant entry.
    """
    mediaFileId: uuid.UUID
    variantName: str = Field(..., max_length=50)
    width: int
    height: int
    fileSizeBytes: int
    storagePath: str = Field(..., max_length=500)
    publicUrl: str = Field(..., max_length=1000)


class MediaVariantUpdate(BaseModel):
    """
    Schema for validating input when updating an existing MediaVariant.
    """
    mediaFileId: uuid.UUID | None = None
    variantName: str | None = Field(None, max_length=50)
    width: int | None = None
    height: int | None = None
    fileSizeBytes: int | None = None
    storagePath: str | None = Field(None, max_length=500)
    publicUrl: str | None = Field(None, max_length=1000)


class MediaVariantResponse(BaseModel):
    """
    Schema representing the structure of a MediaVariant returned in API responses.
    """
    # Configure Pydantic to read ORM models automatically
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    mediaFileId: uuid.UUID
    variantName: str
    width: int
    height: int
    fileSizeBytes: int
    storagePath: str
    publicUrl: str
    createdAt: datetime

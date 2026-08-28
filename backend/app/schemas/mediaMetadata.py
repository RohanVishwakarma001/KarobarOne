# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA METADATA SCHEMAS (mediaMetadata.py)
================================================================================
Why this file is used:
- This file contains the Pydantic validation models for creating, updating, and 
  representing `MediaMetadata` entities.
- It ensures input payload validity for alt text, captions, and slugs.
================================================================================
"""

# Standard library imports for UUIDs and datetime format validations
import uuid
from datetime import datetime

# Third-party Pydantic components for data validation and schema creation
from pydantic import BaseModel, ConfigDict, Field


class MediaMetadataCreate(BaseModel):
    """
    Schema for validating input when creating a new MediaMetadata entry.
    """
    mediaFileId: uuid.UUID
    altText: str | None = Field(None, max_length=255)
    caption: str | None = Field(None, max_length=500)
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    slug: str | None = Field(None, max_length=255)


class MediaMetadataUpdate(BaseModel):
    """
    Schema for validating input when updating an existing MediaMetadata.
    """
    altText: str | None = Field(None, max_length=255)
    caption: str | None = Field(None, max_length=500)
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    slug: str | None = Field(None, max_length=255)


class MediaMetadataResponse(BaseModel):
    """
    Schema representing the structure of a MediaMetadata returned in API responses.
    """
    # Configure Pydantic to read ORM models automatically
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    mediaFileId: uuid.UUID
    altText: str | None
    caption: str | None
    title: str | None
    description: str | None
    slug: str | None
    createdAt: datetime
    updatedAt: datetime

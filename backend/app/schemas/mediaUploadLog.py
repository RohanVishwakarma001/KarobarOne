# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA UPLOAD LOG SCHEMAS (mediaUploadLog.py)
================================================================================
Why this file is used:
- This file contains the Pydantic validation models for creating, updating, and 
  representing `MediaUploadLog` records.
- It ensures structured formatting when logging file chunk upload audits.
================================================================================
"""

# Standard library imports for UUIDs, datetimes, and typing
import uuid
from datetime import datetime
from typing import Any

# Third-party Pydantic components for data validation and schema creation
from pydantic import BaseModel, ConfigDict, Field


class MediaUploadLogCreate(BaseModel):
    """
    Schema for validating input when creating a new MediaUploadLog entry.
    """
    mediaFileId: uuid.UUID
    actionType: str = Field(..., max_length=50)
    performedBy: uuid.UUID
    oldValue: dict[str, Any] | None = None
    newValue: dict[str, Any] | None = None


class MediaUploadLogUpdate(BaseModel):
    """
    Schema for validating input when updating an existing MediaUploadLog.
    """
    mediaFileId: uuid.UUID | None = None
    actionType: str | None = Field(None, max_length=50)
    performedBy: uuid.UUID | None = None
    oldValue: dict[str, Any] | None = None
    newValue: dict[str, Any] | None = None


class MediaUploadLogResponse(BaseModel):
    """
    Schema representing the structure of a MediaUploadLog returned in API responses.
    """
    # Configure Pydantic to read ORM models automatically
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    mediaFileId: uuid.UUID
    actionType: str
    performedBy: uuid.UUID
    oldValue: dict[str, Any] | None
    newValue: dict[str, Any] | None
    createdAt: datetime

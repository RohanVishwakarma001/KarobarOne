# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA FILE SCHEMAS (mediaFile.py)
================================================================================
Why this file is used:
- This file contains the Pydantic schemas used for validation of requests and responses 
  related to the `MediaFile` entity.
- It ensures type safety and input sanitization when creating, updating, or returning
  media file records through the API.
================================================================================
"""

# Standard library imports for UUIDs and datetime format validations
import uuid
from datetime import datetime

# Third-party Pydantic components for data validation and schema creation
from pydantic import BaseModel, ConfigDict, Field


class MediaFileCreate(BaseModel):
    """
    Schema for validating input when creating a new MediaFile entry.
    """
    tenantId: uuid.UUID
    folderName: str | None = Field(None, max_length=100)
    fileName: str = Field(..., max_length=255)
    originalFileName: str = Field(..., max_length=255)
    fileExtension: str = Field(..., max_length=20)
    mimeType: str = Field(..., max_length=100)
    fileSizeBytes: int
    storageProvider: str = Field(..., max_length=50)
    storagePath: str = Field(..., max_length=500)
    publicUrl: str = Field(..., max_length=1000)
    checksumHash: str = Field(..., max_length=128)
    approvalStatus: str = Field("PENDING", max_length=20)
    approvalStatusChangeBy: uuid.UUID | None = None
    approvalStatusChangeAt: datetime | None = None
    uploadedBy: uuid.UUID
    isActive: bool = True


class MediaFileUpdate(BaseModel):
    """
    Schema for validating input when patching/updating an existing MediaFile.
    All attributes are optional.
    """
    folderName: str | None = Field(None, max_length=100)
    fileName: str | None = Field(None, max_length=255)
    originalFileName: str | None = Field(None, max_length=255)
    fileExtension: str | None = Field(None, max_length=20)
    mimeType: str | None = Field(None, max_length=100)
    fileSizeBytes: int | None = None
    storageProvider: str | None = Field(None, max_length=50)
    storagePath: str | None = Field(None, max_length=500)
    publicUrl: str | None = Field(None, max_length=1000)
    checksumHash: str | None = Field(None, max_length=128)
    approvalStatus: str | None = Field(None, max_length=20)
    approvalStatusChangeBy: uuid.UUID | None = None
    approvalStatusChangeAt: datetime | None = None
    uploadedBy: uuid.UUID | None = None
    isActive: bool | None = None


class MediaFileResponse(BaseModel):
    """
    Schema representing the structure of a MediaFile returned in API responses.
    """
    # Configure Pydantic to read ORM models automatically
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenantId: uuid.UUID
    folderName: str | None
    fileName: str
    originalFileName: str
    fileExtension: str
    mimeType: str
    fileSizeBytes: int
    storageProvider: str
    storagePath: str
    publicUrl: str
    checksumHash: str
    approvalStatus: str
    approvalStatusChangeBy: uuid.UUID | None
    approvalStatusChangeAt: datetime | None
    uploadedBy: uuid.UUID
    isActive: bool
    createdAt: datetime
    updatedAt: datetime
    deletedAt: datetime | None

# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA FILES ENDPOINTS ROUTER (mediaFiles.py)
================================================================================
Why this file is used:
- This file defines the REST API routes for interacting with `MediaFile` resources.
- It exposes GET, POST, PATCH, and DELETE endpoints to manage uploaded assets.
================================================================================
"""

# Standard library import for UUID validation
import uuid

# Third-party FastAPI routing and dependency injection tools
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

# Database session dependency
from app.db.session import getDb

# Data validation schemas
from app.schemas.mediaFile import MediaFileCreate, MediaFileResponse, MediaFileUpdate

# Business logic service layer
from app.services.mediaFileService import MediaFileService

# Initialize the router instance with prefix and tags for Swagger UI
router = APIRouter(prefix="/media-files", tags=["Media Files"])


@router.post("/", response_model=MediaFileResponse, status_code=status.HTTP_201_CREATED)
async def createMediaFile(
    data: MediaFileCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Creates a new MediaFile record in the database.
    
    Args:
        data (MediaFileCreate): Input validation model.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaFileResponse: The created media file.
    """
    service = MediaFileService(session)
    return await service.createMediaFile(data)


@router.get("/{mediaFileId}", response_model=MediaFileResponse)
async def getMediaFile(
    mediaFileId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves a MediaFile details by its UUID.
    
    Args:
        mediaFileId (UUID): Unique ID of the media file.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaFileResponse: The retrieved media file.
    """
    service = MediaFileService(session)
    return await service.getMediaFile(mediaFileId)


@router.get("/", response_model=list[MediaFileResponse])
async def listMediaFiles(
    tenantId: uuid.UUID | None = Query(None),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists all MediaFile records, optionally filtered by tenant.
    
    Args:
        tenantId (UUID | None): Optional tenant filter parameter.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        list[MediaFileResponse]: A list of media files.
    """
    service = MediaFileService(session)
    return await service.listMediaFiles(tenantId=tenantId)


@router.patch("/{mediaFileId}", response_model=MediaFileResponse)
async def updateMediaFile(
    mediaFileId: uuid.UUID,
    data: MediaFileUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates attributes of a MediaFile record.
    
    Args:
        mediaFileId (UUID): Unique ID of the media file to update.
        data (MediaFileUpdate): Target update fields.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaFileResponse: The updated media file.
    """
    service = MediaFileService(session)
    return await service.updateMediaFile(mediaFileId, data)


@router.delete("/{mediaFileId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteMediaFile(
    mediaFileId: uuid.UUID,
    soft: bool = Query(True),
    session: AsyncSession = Depends(getDb),
):
    """
    Deletes a MediaFile record (soft delete by default, optionally hard delete).
    
    Args:
        mediaFileId (UUID): Unique ID of the media file to delete.
        soft (bool): Performs a soft-delete if True. Defaults to True.
        session (AsyncSession): Database session injected dependency.
    """
    service = MediaFileService(session)
    await service.deleteMediaFile(mediaFileId, soft=soft)

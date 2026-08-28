# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA UPLOAD LOGS ENDPOINTS ROUTER (mediaUploadLogs.py)
================================================================================
Why this file is used:
- This file defines the REST API routes for interacting with `MediaUploadLog` resources.
- It exposes GET, POST, PATCH, and DELETE endpoints for file upload audit history.
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
from app.schemas.mediaUploadLog import MediaUploadLogCreate, MediaUploadLogResponse, MediaUploadLogUpdate

# Business logic service layer
from app.services.mediaUploadLogService import MediaUploadLogService

# Initialize the router instance with prefix and tags for Swagger UI
router = APIRouter(prefix="/media-upload-logs", tags=["Media Upload Logs"])


@router.post("/", response_model=MediaUploadLogResponse, status_code=status.HTTP_201_CREATED)
async def createMediaUploadLog(
    data: MediaUploadLogCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Creates a new MediaUploadLog record in the database.
    
    Args:
        data (MediaUploadLogCreate): Input validation model.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaUploadLogResponse: The created upload log record.
    """
    service = MediaUploadLogService(session)
    return await service.createMediaUploadLog(data)


@router.get("/{logId}", response_model=MediaUploadLogResponse)
async def getMediaUploadLog(
    logId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves a MediaUploadLog by its UUID.
    
    Args:
        logId (UUID): Unique ID of the upload log.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaUploadLogResponse: The retrieved upload log record.
    """
    service = MediaUploadLogService(session)
    return await service.getMediaUploadLog(logId)


@router.get("/", response_model=list[MediaUploadLogResponse])
async def listMediaUploadLogs(
    mediaFileId: uuid.UUID | None = Query(None),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists all MediaUploadLog records, optionally filtered by parent media file.
    
    Args:
        mediaFileId (UUID | None): Optional media file filter parameter.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        list[MediaUploadLogResponse]: A list of upload log records.
    """
    service = MediaUploadLogService(session)
    return await service.listMediaUploadLogs(mediaFileId=mediaFileId)


@router.patch("/{logId}", response_model=MediaUploadLogResponse)
async def updateMediaUploadLog(
    logId: uuid.UUID,
    data: MediaUploadLogUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates attributes of a MediaUploadLog record.
    
    Args:
        logId (UUID): Unique ID of the upload log to update.
        data (MediaUploadLogUpdate): Target update fields.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaUploadLogResponse: The updated upload log record.
    """
    service = MediaUploadLogService(session)
    return await service.updateMediaUploadLog(logId, data)


@router.delete("/{logId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteMediaUploadLog(
    logId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Hard deletes a MediaUploadLog record.
    
    Args:
        logId (UUID): Unique ID of the upload log to delete.
        session (AsyncSession): Database session injected dependency.
    """
    service = MediaUploadLogService(session)
    await service.deleteMediaUploadLog(logId)

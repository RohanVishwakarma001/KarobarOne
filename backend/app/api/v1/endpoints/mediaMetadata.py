# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA METADATA ENDPOINTS ROUTER (mediaMetadata.py)
================================================================================
Why this file is used:
- This file defines the REST API routes for interacting with `MediaMetadata` resources.
- It exposes endpoints to create, fetch, update, and delete ALT tags and titles for media.
================================================================================
"""

# Standard library import for UUID validation
import uuid

# Third-party FastAPI routing and dependency injection tools
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Database session dependency
from app.db.session import getDb

# Data validation schemas
from app.schemas.mediaMetadata import MediaMetadataCreate, MediaMetadataResponse, MediaMetadataUpdate

# Business logic service layer
from app.services.mediaMetadataService import MediaMetadataService

# Initialize the router instance with prefix and tags for Swagger UI
router = APIRouter(prefix="/media-metadata", tags=["Media Metadata"])


@router.post("/", response_model=MediaMetadataResponse, status_code=status.HTTP_201_CREATED)
async def createMediaMetadata(
    data: MediaMetadataCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Creates a new MediaMetadata record associated with a parent MediaFile.
    
    Args:
        data (MediaMetadataCreate): Input validation model.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaMetadataResponse: The created media metadata record.
    """
    service = MediaMetadataService(session)
    return await service.createMediaMetadata(data)


@router.get("/{metadataId}", response_model=MediaMetadataResponse)
async def getMediaMetadata(
    metadataId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves a MediaMetadata record by its unique UUID.
    
    Args:
        metadataId (UUID): Unique ID of the metadata record.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaMetadataResponse: The retrieved metadata record.
    """
    service = MediaMetadataService(session)
    return await service.getMediaMetadata(metadataId)


@router.get("/media-file/{mediaFileId}", response_model=MediaMetadataResponse)
async def getMediaMetadataByMediaFile(
    mediaFileId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves a MediaMetadata record by its parent Media File ID.
    
    Args:
        mediaFileId (UUID): Unique ID of the parent media file.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaMetadataResponse: The retrieved metadata record.
    """
    service = MediaMetadataService(session)
    return await service.getMediaMetadataByMediaFile(mediaFileId)


@router.get("/", response_model=list[MediaMetadataResponse])
async def listMediaMetadata(
    session: AsyncSession = Depends(getDb),
):
    """
    Lists all MediaMetadata records in the system.
    
    Args:
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        list[MediaMetadataResponse]: A list of metadata records.
    """
    service = MediaMetadataService(session)
    return await service.listMediaMetadata()


@router.patch("/{metadataId}", response_model=MediaMetadataResponse)
async def updateMediaMetadata(
    metadataId: uuid.UUID,
    data: MediaMetadataUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates fields of an existing MediaMetadata record.
    
    Args:
        metadataId (UUID): Unique ID of the metadata record to update.
        data (MediaMetadataUpdate): Target update fields.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaMetadataResponse: The updated metadata record.
    """
    service = MediaMetadataService(session)
    return await service.updateMediaMetadata(metadataId, data)


@router.delete("/{metadataId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteMediaMetadata(
    metadataId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Hard deletes a MediaMetadata record.
    
    Args:
        metadataId (UUID): Unique ID of the metadata record to delete.
        session (AsyncSession): Database session injected dependency.
    """
    service = MediaMetadataService(session)
    await service.deleteMediaMetadata(metadataId)

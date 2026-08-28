# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA VARIANTS ENDPOINTS ROUTER (mediaVariants.py)
================================================================================
Why this file is used:
- This file defines the REST API routes for interacting with `MediaVariant` resources.
- It exposes endpoints to create, fetch, update, and delete image size configurations.
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
from app.schemas.mediaVariant import MediaVariantCreate, MediaVariantResponse, MediaVariantUpdate

# Business logic service layer
from app.services.mediaVariantService import MediaVariantService

# Initialize the router instance with prefix and tags for Swagger UI
router = APIRouter(prefix="/media-variants", tags=["Media Variants"])


@router.post("/", response_model=MediaVariantResponse, status_code=status.HTTP_201_CREATED)
async def createMediaVariant(
    data: MediaVariantCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Creates a new MediaVariant record linked to a parent MediaFile.
    
    Args:
        data (MediaVariantCreate): Input validation model.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaVariantResponse: The created variant record.
    """
    service = MediaVariantService(session)
    return await service.createMediaVariant(data)


@router.get("/{variantId}", response_model=MediaVariantResponse)
async def getMediaVariant(
    variantId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves a MediaVariant details by its UUID.
    
    Args:
        variantId (UUID): Unique ID of the variant.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaVariantResponse: The retrieved variant record.
    """
    service = MediaVariantService(session)
    return await service.getMediaVariant(variantId)


@router.get("/", response_model=list[MediaVariantResponse])
async def listMediaVariants(
    mediaFileId: uuid.UUID | None = Query(None),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists all MediaVariant records, optionally filtered by parent media file.
    
    Args:
        mediaFileId (UUID | None): Optional media file ID filter parameter.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        list[MediaVariantResponse]: A list of variant records.
    """
    service = MediaVariantService(session)
    return await service.listMediaVariants(mediaFileId=mediaFileId)


@router.patch("/{variantId}", response_model=MediaVariantResponse)
async def updateMediaVariant(
    variantId: uuid.UUID,
    data: MediaVariantUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates dimensions or storage attributes of a MediaVariant.
    
    Args:
        variantId (UUID): Unique ID of the variant to update.
        data (MediaVariantUpdate): Target update fields.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        MediaVariantResponse: The updated variant record.
    """
    service = MediaVariantService(session)
    return await service.updateMediaVariant(variantId, data)


@router.delete("/{variantId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteMediaVariant(
    variantId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Hard deletes a MediaVariant record.
    
    Args:
        variantId (UUID): Unique ID of the variant to delete.
        session (AsyncSession): Database session injected dependency.
    """
    service = MediaVariantService(session)
    await service.deleteMediaVariant(variantId)

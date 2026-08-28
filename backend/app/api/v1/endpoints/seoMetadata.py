# Owner: mousamdas156@gmail.com
"""
================================================================================
SEO METADATA ENDPOINTS ROUTER (seoMetadata.py)
================================================================================
Why this file is used:
- This file defines the REST API routes for interacting with `SeoMetadata` resources.
- It exposes endpoints to create, fetch, search by slug/entity, update, and delete SEO attributes.
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
from app.schemas.seoMetadata import (
    SeoMetadataCreate,
    SeoMetadataResponse,
    SeoMetadataUpdate,
    SeoScoreRequest,
    SeoScoreResponse,
    AiSeoSuggestionRequest,
    AiSeoSuggestionResponse,
    SeoAuditRequest,
    SeoAuditResponse,
    KeywordDensityRequest,
    KeywordDensityResponse,
)

# Business logic service layer
from app.services.seoMetadataService import SeoMetadataService

# Initialize the router instance with prefix and tags for Swagger UI
router = APIRouter(prefix="/seo-metadata", tags=["SEO Metadata"])


@router.post("/", response_model=SeoMetadataResponse, status_code=status.HTTP_201_CREATED)
async def createSeoMetadata(
    data: SeoMetadataCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Creates a new SeoMetadata record in the system.
    
    Args:
        data (SeoMetadataCreate): Input validation model.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        SeoMetadataResponse: The created SEO metadata.
    """
    service = SeoMetadataService(session)
    return await service.createSeoMetadata(data)


@router.get("/{seoId}", response_model=SeoMetadataResponse)
async def getSeoMetadata(
    seoId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves an SEO record by its UUID.
    
    Args:
        seoId (UUID): Unique ID of the SEO record.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        SeoMetadataResponse: The retrieved SEO metadata.
    """
    service = SeoMetadataService(session)
    return await service.getSeoMetadata(seoId)


@router.get("/entity/{entityType}/{entityId}", response_model=SeoMetadataResponse)
async def getSeoMetadataByEntity(
    entityType: str,
    entityId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves an SEO record by entity type and entity UUID.
    
    Args:
        entityType (str): Type of entity (e.g. 'PRODUCT').
        entityId (UUID): Unique ID of the target resource.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        SeoMetadataResponse: The retrieved SEO metadata.
    """
    service = SeoMetadataService(session)
    return await service.getSeoMetadataByEntity(entityType, entityId)


@router.get("/slug/{entityType}/{slug}", response_model=SeoMetadataResponse)
async def getSeoMetadataBySlug(
    entityType: str,
    slug: str,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves an SEO record by entity type and URL slug.
    
    Args:
        entityType (str): Type of entity (e.g. 'BLOG').
        slug (str): Route slug path.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        SeoMetadataResponse: The retrieved SEO metadata.
    """
    service = SeoMetadataService(session)
    return await service.getSeoMetadataBySlug(entityType, slug)


@router.get("/", response_model=list[SeoMetadataResponse])
async def listSeoMetadata(
    tenantId: uuid.UUID | None = Query(None),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists all SEO records, optionally filtered by tenant.
    
    Args:
        tenantId (UUID | None): Optional tenant ID filter parameter.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        list[SeoMetadataResponse]: A list of SEO metadata records.
    """
    service = SeoMetadataService(session)
    return await service.listSeoMetadata(tenantId=tenantId)


@router.patch("/{seoId}", response_model=SeoMetadataResponse)
async def updateSeoMetadata(
    seoId: uuid.UUID,
    data: SeoMetadataUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates search preferences on an existing SEO record.
    
    Args:
        seoId (UUID): Unique ID of the SEO record to update.
        data (SeoMetadataUpdate): Target update fields.
        session (AsyncSession): Database session injected dependency.
        
    Returns:
        SeoMetadataResponse: The updated SEO metadata.
    """
    service = SeoMetadataService(session)
    return await service.updateSeoMetadata(seoId, data)


@router.delete("/{seoId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteSeoMetadata(
    seoId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Hard deletes an SEO record.
    
    Args:
        seoId (UUID): Unique ID of the SEO record to delete.
        session (AsyncSession): Database session injected dependency.
    """
    service = SeoMetadataService(session)
    await service.deleteSeoMetadata(seoId)
@router.post("/score", response_model=SeoScoreResponse)
async def calculateSeoScore(
    data: SeoScoreRequest,
    session: AsyncSession = Depends(getDb),
):
    service = SeoMetadataService(session)
    return await service.calculateSeoScore(data)


@router.post("/ai-suggestions", response_model=AiSeoSuggestionResponse)
async def generateAiSeoSuggestions(
    data: AiSeoSuggestionRequest,
    session: AsyncSession = Depends(getDb),
):
    service = SeoMetadataService(session)
    return await service.generateAiSeoSuggestions(data)


@router.post("/audit", response_model=SeoAuditResponse)
async def auditSeo(
    data: SeoAuditRequest,
    session: AsyncSession = Depends(getDb),
):
    service = SeoMetadataService(session)
    return await service.auditSeo(data)


@router.post("/keyword-density", response_model=KeywordDensityResponse)
async def keywordDensity(
    data: KeywordDensityRequest,
    session: AsyncSession = Depends(getDb),
):
    service = SeoMetadataService(session)
    return await service.analyzeKeywordDensity(data)

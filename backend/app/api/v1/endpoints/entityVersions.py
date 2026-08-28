# Owner - pradhansaikat123@gmail.com
# ================================================================================
# FILE: api/v1/endpoints/entityVersions.py — Entity Version Endpoints
# ================================================================================
# Why this file is used:
#   - Exposes REST API endpoints for fetching version snapshots and triggering
#     historical rollbacks.
#
# What components are inside:
#   - POST /            -> Create a new entity version snapshot manually
#   - GET /             -> List entity versions with pagination and filtering
#   - GET /{id}         -> Fetch details of a specific entity version
#   - POST /{id}/rollback -> Restore entity state to a historical version snapshot
# ================================================================================
"""
Endpoints for managing historical entity version snapshots.
"""

# Import List and Optional wrappers for endpoint signature annotations
from typing import List, Optional
# Import UUID class for typing path variable identifiers
from uuid import UUID
# Import FastAPI components for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import AsyncSession for database operations
from sqlalchemy.ext.asyncio import AsyncSession

# Import DB session provider dependency
from app.db.session import getDb as get_db
# Import EntityVersion model definition
from app.db.models.approvals import EntityVersion
# Import schemas for validation and responses
from app.schemas.approvals import (
    EntityVersionCreate,
    EntityVersionResponse,
    EntityVersionUpdate,
)

# owner: mousamdas156@gmail.com
# Import rollback schemas, service, and custom exceptions
from app.schemas.approvals import RollbackPayload
from app.services.approvalService import ApprovalService
from app.core.exceptionsCompat import NotFoundError, BusinessValidationError

router = APIRouter(prefix="/entity-versions", tags=["Entity Versions"])


@router.post("/", response_model=EntityVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_entity_version(
    payload: EntityVersionCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Manually creates a new entity version record.
    """
    dbVersion = EntityVersion(**payload.model_dump())
    db.add(dbVersion)
    await db.commit()
    await db.refresh(dbVersion)
    return dbVersion


@router.get("/", response_model=List[EntityVersionResponse])
async def list_entity_versions(
    tenantId: Optional[UUID] = None,
    entityType: Optional[str] = None,
    entityId: Optional[UUID] = None,
    isPublished: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    Lists historical entity version records with filtering and pagination.
    """
    query = select(EntityVersion)
    if tenantId:
        query = query.where(EntityVersion.tenantId == tenantId)
    if entityType:
        query = query.where(EntityVersion.entityType == entityType)
    if entityId:
        query = query.where(EntityVersion.entityId == entityId)
    if isPublished is not None:
        query = query.where(EntityVersion.isPublished == isPublished)

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/preview", response_model=EntityVersionResponse)
async def preview_entity_version(
    entityType: str,
    entityId: UUID,
    tenantId: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    TC-0113 Preview Endpoint:
    Retrieves the latest pending/unpublished entity version snapshot for previewing
    unapproved changes before publication. If no unpublished version exists, falls
    back to the latest version record.
    """
    # First look for latest unpublished version snapshot (pending approval)
    query = select(EntityVersion).where(
        EntityVersion.entityType == entityType,
        EntityVersion.entityId == entityId,
        EntityVersion.isPublished == False
    )
    if tenantId:
        query = query.where(EntityVersion.tenantId == tenantId)
    
    query = query.order_by(EntityVersion.versionNumber.desc())
    result = await db.execute(query)
    previewVersion = result.scalars().first()

    # Fallback to latest version if no draft/unpublished version exists
    if not previewVersion:
        query_all = select(EntityVersion).where(
            EntityVersion.entityType == entityType,
            EntityVersion.entityId == entityId
        )
        if tenantId:
            query_all = query_all.where(EntityVersion.tenantId == tenantId)
        query_all = query_all.order_by(EntityVersion.versionNumber.desc())
        res_all = await db.execute(query_all)
        previewVersion = res_all.scalars().first()

    if not previewVersion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No preview version found for entity {entityType}:{entityId}"
        )
    return previewVersion


@router.get("/{versionId}", response_model=EntityVersionResponse)
async def get_entity_version(
    versionId: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieves detail of a single entity version snapshot.
    """
    result = await db.execute(select(EntityVersion).where(EntityVersion.id == versionId))
    dbVersion = result.scalar_one_or_none()
    if not dbVersion:
        raise HTTPException(status_code=404, detail="Entity version not found")
    return dbVersion


# owner: mousamdas156@gmail.com
# Rollback historical version endpoint
@router.post("/{versionId}/rollback", response_model=EntityVersionResponse)
async def rollback_entity_version(
    versionId: UUID,
    payload: RollbackPayload,
    db: AsyncSession = Depends(get_db),
):
    """
    Restores the live entity state to matches this historical version snapshot.
    Generates a new published EntityVersion row and records a RESTORE audit log.
    """
    service = ApprovalService(db)
    try:
        new_published_version = await service.rollbackEntity(
            versionId=versionId,
            performedBy=payload.performedBy,
        )
        return new_published_version
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )




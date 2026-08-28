# Owner - pradhansaikat123@gmail.com
# Tag mappings router. Manages associations between tags and various database entities,
# ensuring target tags are active and preventing duplicate mapping creation.

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb as get_db
from app.db.models.tags import Tag, TagMapping
from app.schemas.tags import (
    PaginatedResponse,
    TagMappingCreate,
    TagMappingResponse,
)

router = APIRouter(prefix="/tag-mappings", tags=["Tag Mappings"])


# ── CREATE ───────────────────────────────────
@router.post("/", response_model=TagMappingResponse, status_code=status.HTTP_201_CREATED)
async def create_mapping(payload: TagMappingCreate, db: AsyncSession = Depends(get_db)):
    # 1. Verify target tag exists, is active, and is not deleted
    tag_result = await db.execute(
        select(Tag).where(Tag.id == payload.tagId, Tag.deletedAt.is_(None))
    )
    tag = tag_result.scalar_one_or_none()
    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Target tag not found or has been deleted",
        )
    if not tag.isActive:
        raise HTTPException(
            status_code=400,
            detail="Cannot map to an inactive tag",
        )

    # 2. Check for duplicate mapping
    dup_result = await db.execute(
        select(TagMapping).where(
            TagMapping.tagId == payload.tagId,
            TagMapping.entityType == payload.entityType,
            TagMapping.entityId == payload.entityId,
        )
    )
    if dup_result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="This entity is already mapped to the specified tag",
        )

    mapping = TagMapping(**payload.model_dump())
    db.add(mapping)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        err_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        raise HTTPException(
            status_code=400,
            detail=f"Database integrity error: {err_msg}",
        )

    await db.refresh(mapping)
    return mapping


# ── LIST (paginated) ─────────────────────────
@router.get("/", response_model=PaginatedResponse)
async def list_mappings(
    tagId: Optional[UUID] = Query(None),
    entityType: Optional[str] = Query(None),
    entityId: Optional[UUID] = Query(None),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(TagMapping)

    if tagId is not None:
        query = query.where(TagMapping.tagId == tagId)
    if entityType:
        query = query.where(TagMapping.entityType == entityType)
    if entityId is not None:
        query = query.where(TagMapping.entityId == entityId)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Fetch paginated details
    result = await db.execute(
        query.order_by(TagMapping.createdAt.desc())
        .offset((page - 1) * pageSize)
        .limit(pageSize)
    )
    mappings = result.scalars().all()

    return {"total": total, "page": page, "pageSize": pageSize, "data": mappings}


# ── GET BY ID ────────────────────────────────
@router.get("/{mapping_id}", response_model=TagMappingResponse)
async def get_mapping(mapping_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TagMapping).where(TagMapping.id == mapping_id)
    )
    mapping = result.scalar_one_or_none()
    if not mapping:
        raise HTTPException(status_code=404, detail="Tag mapping not found")
    return mapping


# ── DELETE ───────────────────────────────────
@router.delete("/{mapping_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mapping(mapping_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TagMapping).where(TagMapping.id == mapping_id)
    )
    mapping = result.scalar_one_or_none()
    if not mapping:
        raise HTTPException(status_code=404, detail="Tag mapping not found")

    await db.delete(mapping)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error deleting tag mapping: {str(e)}",
        )

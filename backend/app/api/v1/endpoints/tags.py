# Owner - pradhansaikat123@gmail.com
# Tag router endpoints. Implements tag creation (with slugify logic), paginated filtering,
# fetch by ID, update, and soft-delete features.

import re
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb as get_db
from app.db.models.tags import Tag
from app.schemas.tags import (
    PaginatedResponse,
    TagCreate,
    TagResponse,
    TagUpdate,
)

router = APIRouter(prefix="/tags", tags=["Tags"])


def slugify(text: str) -> str:
    """Helper to convert tagName to a URL-friendly slug."""
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return s.strip("-")


# ── CREATE ───────────────────────────────────
@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(payload: TagCreate, db: AsyncSession = Depends(get_db)):
    slug = payload.tagSlug or slugify(payload.tagName)
    if not slug:
        raise HTTPException(
            status_code=400,
            detail="Could not generate a valid slug from the provided tag name",
        )

    # 1. Duplicate check: store_id + tag_type + tag_name
    name_check_query = select(Tag).where(
        Tag.tagType == payload.tagType,
        Tag.tagName == payload.tagName,
        Tag.deletedAt.is_(None),
    )
    if payload.storeId:
        name_check_query = name_check_query.where(Tag.storeId == payload.storeId)
    else:
        name_check_query = name_check_query.where(Tag.storeId.is_(None))

    name_check_result = await db.execute(name_check_query)
    if name_check_result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"Tag with name '{payload.tagName}' already exists for this type and store",
        )

    # 2. Duplicate check: store_id + tag_type + tag_slug
    slug_check_query = select(Tag).where(
        Tag.tagType == payload.tagType,
        Tag.tagSlug == slug,
        Tag.deletedAt.is_(None),
    )
    if payload.storeId:
        slug_check_query = slug_check_query.where(Tag.storeId == payload.storeId)
    else:
        slug_check_query = slug_check_query.where(Tag.storeId.is_(None))

    slug_check_result = await db.execute(slug_check_query)
    if slug_check_result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"Tag with slug '{slug}' already exists for this type and store",
        )

    data = payload.model_dump()
    data["tagSlug"] = slug

    tag = Tag(**data)
    db.add(tag)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        err_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        raise HTTPException(
            status_code=400,
            detail=f"Database integrity error: {err_msg}",
        )

    await db.refresh(tag)
    return tag


# ── LIST (paginated) ─────────────────────────
@router.get("/", response_model=PaginatedResponse)
async def list_tags(
    storeId: Optional[UUID] = Query(None),
    tenantId: Optional[UUID] = Query(None),
    tagType: Optional[str] = Query(None),
    isActive: Optional[bool] = Query(None),
    isSystemTag: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Tag).where(Tag.deletedAt.is_(None))

    if storeId is not None:
        query = query.where(Tag.storeId == storeId)
    if tenantId is not None:
        query = query.where(Tag.tenantId == tenantId)
    if tagType:
        query = query.where(Tag.tagType == tagType)
    if isActive is not None:
        query = query.where(Tag.isActive == isActive)
    if isSystemTag is not None:
        query = query.where(Tag.isSystemTag == isSystemTag)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Fetch paginated details
    result = await db.execute(
        query.order_by(Tag.createdAt.desc())
        .offset((page - 1) * pageSize)
        .limit(pageSize)
    )
    tags = result.scalars().all()

    return {"total": total, "page": page, "pageSize": pageSize, "data": tags}


# ── GET BY ID ────────────────────────────────
@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id, Tag.deletedAt.is_(None))
    )
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


# ── UPDATE ───────────────────────────────────
@router.patch("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: UUID, payload: TagUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id, Tag.deletedAt.is_(None))
    )
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    update_data = payload.model_dump(exclude_none=True)

    # Determine tag type, name, slug and store_id to validate uniqueness if name or slug or storeId changes
    current_name = update_data.get("tagName", tag.tagName)
    current_slug = update_data.get("tagSlug", tag.tagSlug)
    current_type = update_data.get("tagType", tag.tagType)
    current_store = tag.storeId  # Note: storeId cannot be updated via Patch according to TagUpdate schema

    # Re-slugify if name was updated but not the slug explicitly
    if "tagName" in update_data and "tagSlug" not in update_data:
        current_slug = slugify(update_data["tagName"])
        update_data["tagSlug"] = current_slug

    # Validate duplicates if name/slug was updated
    if "tagName" in update_data:
        name_check_query = select(Tag).where(
            Tag.id != tag_id,
            Tag.tagType == current_type,
            Tag.tagName == current_name,
            Tag.deletedAt.is_(None),
        )
        if current_store:
            name_check_query = name_check_query.where(Tag.storeId == current_store)
        else:
            name_check_query = name_check_query.where(Tag.storeId.is_(None))

        name_check_result = await db.execute(name_check_query)
        if name_check_result.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail=f"Tag with name '{current_name}' already exists for this type and store",
            )

    if "tagSlug" in update_data or "tagName" in update_data:
        slug_check_query = select(Tag).where(
            Tag.id != tag_id,
            Tag.tagType == current_type,
            Tag.tagSlug == current_slug,
            Tag.deletedAt.is_(None),
        )
        if current_store:
            slug_check_query = slug_check_query.where(Tag.storeId == current_store)
        else:
            slug_check_query = slug_check_query.where(Tag.storeId.is_(None))

        slug_check_result = await db.execute(slug_check_query)
        if slug_check_result.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail=f"Tag with slug '{current_slug}' already exists for this type and store",
            )

    for field, value in update_data.items():
        setattr(tag, field, value)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        err_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        raise HTTPException(
            status_code=400,
            detail=f"Database integrity error: {err_msg}",
        )

    await db.refresh(tag)
    return tag


# ── SOFT DELETE ──────────────────────────────
@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id, Tag.deletedAt.is_(None))
    )
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.deletedAt = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error deleting tag: {str(e)}",
        )

# Owner - pradhansaikat123@gmail.com
import re  # Regular expressions library
from datetime import datetime, timezone  # Datetime utilities
from typing import List, Optional  # Type annotations
from uuid import UUID  # UUID helper

from fastapi import APIRouter, Depends, HTTPException, Query, status  # FastAPI router and dependencies
from sqlalchemy import func, select  # SQLAlchemy query helpers
from sqlalchemy.exc import IntegrityError  # DB integrity error handling
from sqlalchemy.ext.asyncio import AsyncSession  # Async database session

from app.db.session import getDb as get_db  # Session local generator
from app.db.models.categories import Category  # Category database model
from app.schemas.categories import (  # Pydantic schema validation objects
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    PaginatedResponse,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


def slugify(text: str) -> str:
    """Helper to convert categoryName to a URL-friendly slug."""
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return s.strip("-")


# ── CREATE ───────────────────────────────────
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreate, db: AsyncSession = Depends(get_db)):
    slug = payload.categorySlug or slugify(payload.categoryName)
    if not slug:
        raise HTTPException(
            status_code=400,
            detail="Could not generate a valid slug from the provided category name",
        )

    # 1. Duplicate check: storeId + categoryName
    nameCheckQuery = select(Category).where(
        Category.categoryName == payload.categoryName,
        Category.deletedAt.is_(None),
    )
    if payload.storeId:
        nameCheckQuery = nameCheckQuery.where(Category.storeId == payload.storeId)
    else:
        nameCheckQuery = nameCheckQuery.where(Category.storeId.is_(None))

    nameCheckResult = await db.execute(nameCheckQuery)
    if nameCheckResult.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"Category with name '{payload.categoryName}' already exists for this store",
        )

    # 2. Duplicate check: categorySlug (globally unique per DB constraints)
    slugCheckQuery = select(Category).where(
        Category.categorySlug == slug,
        Category.deletedAt.is_(None),
    )

    slugCheckResult = await db.execute(slugCheckQuery)
    if slugCheckResult.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"Category with slug '{slug}' already exists",
        )

    # 3. Parent validation if parentCategoryId is provided
    if payload.parentCategoryId:
        parentResult = await db.execute(
            select(Category).where(
                Category.id == payload.parentCategoryId,
                Category.deletedAt.is_(None)
            )
        )
        parent = parentResult.scalar_one_or_none()
        if not parent:
            raise HTTPException(
                status_code=404,
                detail=f"Parent category with id {payload.parentCategoryId} not found"
            )

    data = payload.model_dump()
    data["categorySlug"] = slug

    category = Category(**data)
    db.add(category)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        errMsg = str(e.orig) if hasattr(e, "orig") else str(e)
        raise HTTPException(
            status_code=400,
            detail=f"Database integrity error: {errMsg}",
        )

    await db.refresh(category)
    return category


# ── LIST (paginated) ─────────────────────────
@router.get("/", response_model=PaginatedResponse)
async def list_categories(
    storeId: Optional[UUID] = Query(None),
    tenantId: Optional[UUID] = Query(None),
    parentCategoryId: Optional[UUID] = Query(None),
    categoryType: Optional[str] = Query(None),
    isActive: Optional[bool] = Query(None),
    isSystemCategory: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Category).where(Category.deletedAt.is_(None))

    if storeId is not None:
        query = query.where(Category.storeId == storeId)
    if tenantId is not None:
        query = query.where(Category.tenantId == tenantId)
    if parentCategoryId is not None:
        query = query.where(Category.parentCategoryId == parentCategoryId)
    if categoryType:
        query = query.where(Category.categoryType == categoryType)
    if isActive is not None:
        query = query.where(Category.isActive == isActive)
    if isSystemCategory is not None:
        query = query.where(Category.isSystemCategory == isSystemCategory)

    # Count total
    countQuery = select(func.count()).select_from(query.subquery())
    totalResult = await db.execute(countQuery)
    total = totalResult.scalar()

    # Fetch paginated details
    result = await db.execute(
        query.order_by(Category.displayOrder.asc(), Category.createdAt.desc())
        .offset((page - 1) * pageSize)
        .limit(pageSize)
    )
    categories = result.scalars().all()

    return {"total": total, "page": page, "pageSize": pageSize, "data": categories}


# ── GET BY ID ────────────────────────────────
@router.get("/{categoryId}", response_model=CategoryResponse)
async def get_category(categoryId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category).where(Category.id == categoryId, Category.deletedAt.is_(None))
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# ── UPDATE ───────────────────────────────────
@router.patch("/{categoryId}", response_model=CategoryResponse)
async def update_category(
    categoryId: UUID, payload: CategoryUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Category).where(Category.id == categoryId, Category.deletedAt.is_(None))
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    updateData = payload.model_dump(exclude_none=True)

    # If category name is updated and category slug is not explicitly provided, re-slugify
    currentName = updateData.get("categoryName", category.categoryName)
    currentSlug = updateData.get("categorySlug", category.categorySlug)
    currentStore = category.storeId

    if "categoryName" in updateData and "categorySlug" not in updateData:
        currentSlug = slugify(updateData["categoryName"])
        updateData["categorySlug"] = currentSlug

    # Validate duplicates for categoryName
    if "categoryName" in updateData:
        nameCheckQuery = select(Category).where(
            Category.id != categoryId,
            Category.categoryName == currentName,
            Category.deletedAt.is_(None),
        )
        if currentStore:
            nameCheckQuery = nameCheckQuery.where(Category.storeId == currentStore)
        else:
            nameCheckQuery = nameCheckQuery.where(Category.storeId.is_(None))

        nameCheckResult = await db.execute(nameCheckQuery)
        if nameCheckResult.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail=f"Category with name '{currentName}' already exists for this store",
            )

    # Validate duplicates for categorySlug (globally unique per DB constraints)
    if "categorySlug" in updateData or "categoryName" in updateData:
        slugCheckQuery = select(Category).where(
            Category.id != categoryId,
            Category.categorySlug == currentSlug,
            Category.deletedAt.is_(None),
        )

        slugCheckResult = await db.execute(slugCheckQuery)
        if slugCheckResult.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail=f"Category with slug '{currentSlug}' already exists",
            )

    # If parentCategoryId is being updated, validate it exists
    if "parentCategoryId" in updateData and updateData["parentCategoryId"] is not None:
        parentId = updateData["parentCategoryId"]
        if parentId == categoryId:
            raise HTTPException(
                status_code=400,
                detail="A category cannot be its own parent"
            )
        parentResult = await db.execute(
            select(Category).where(
                Category.id == parentId,
                Category.deletedAt.is_(None)
            )
        )
        parent = parentResult.scalar_one_or_none()
        if not parent:
            raise HTTPException(
                status_code=404,
                detail=f"Parent category with id {parentId} not found"
            )

    # Perform updates
    for field, value in updateData.items():
        setattr(category, field, value)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        errMsg = str(e.orig) if hasattr(e, "orig") else str(e)
        raise HTTPException(
            status_code=400,
            detail=f"Database integrity error: {errMsg}",
        )

    await db.refresh(category)
    return category


# ── SOFT DELETE ──────────────────────────────
@router.delete("/{categoryId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(categoryId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category).where(Category.id == categoryId, Category.deletedAt.is_(None))
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.deletedAt = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error deleting category: {str(e)}",
        )


@router.get("/trash/list", response_model=PaginatedResponse)
async def list_trash_categories(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Category).where(Category.deletedAt.is_not(None))
    countQuery = select(func.count()).select_from(query.subquery())
    totalResult = await db.execute(countQuery)
    total = totalResult.scalar()

    result = await db.execute(
        query.order_by(Category.createdAt.desc())
        .offset((page - 1) * pageSize)
        .limit(pageSize)
    )
    categories = result.scalars().all()
    return {"total": total, "page": page, "pageSize": pageSize, "data": categories}


@router.post("/{categoryId}/restore", response_model=CategoryResponse)
async def restore_category(categoryId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category).where(Category.id == categoryId, Category.deletedAt.is_not(None))
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Deleted category not found")

    category.deletedAt = None
    await db.commit()
    await db.refresh(category)
    return category


# Owner - pradhansaikat123@gmail.com

# Categories API endpoints. Supports CRUD, slug/name uniqueness validation,
# and cycle validation for parent/child hierarchies.

# Import List and Optional from typing for type declarations
from typing import List, Optional
# Import UUID from uuid for unique identifier support
from uuid import UUID
# Import datetime and timezone from datetime for handling dates
from datetime import datetime, timezone

# Import APIRouter, Depends, HTTPException, Query, and status from fastapi
from fastapi import APIRouter, Depends, HTTPException, Query, status
# Import select and func from sqlalchemy for database queries
from sqlalchemy import select, func
# Import AsyncSession from sqlalchemy.ext.asyncio for asynchronous sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import get_db session dependency injection helper
from app.productsPorted.core.database import get_db
# Import Category model from models
from app.productsPorted.models.models import Category
# Import schemas from app schemas
from app.productsPorted.schemas.schemas import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Products - Categories"])


async def validate_category_hierarchy(db: AsyncSession, categoryId: UUID, parentId: UUID):
    """
    Validates that setting parentId for categoryId does not cause a cycle.
    A cycle is formed if the proposed parent is the category itself, 
    or is a descendant of the category.
    """
    if categoryId == parentId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category cannot be its own parent."
        )
    
    # Traverse upwards from proposed parentId. If we encounter categoryId, there is a loop.
    currentParentId = parentId
    while currentParentId is not None:
        result = await db.execute(
            select(Category.parentId).where(Category.id == currentParentId, Category.deletedAt.is_(None))
        )
        # Note: using scalar() or scalar_one_or_none()
        nextParent = result.scalar_one_or_none()
        
        # If the query returned None, this means we either reached the root, or the category is deleted
        if nextParent is None:
            # Let's check if the currentParentId even exists
            checkExist = await db.execute(select(Category.id).where(Category.id == currentParentId, Category.deletedAt.is_(None)))
            if not checkExist.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Proposed parent category does not exist."
                )
            break
            
        if nextParent == categoryId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hierarchy validation failed: setting this parent would create a cyclic loop."
            )
        currentParentId = nextParent


# ── CREATE ───────────────────────────────────
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreate, db: AsyncSession = Depends(get_db)):
    # 1. Parent validation (if exists)
    if payload.parentId:
        res = await db.execute(
            select(Category).where(Category.id == payload.parentId, Category.deletedAt.is_(None))
        )
        if not res.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Parent category not found")

    # 2. Duplicate Check: Name uniqueness under the same parent for the tenant
    dupName = await db.execute(
        select(Category).where(
            Category.tenantId == payload.tenantId,
            Category.parentId == payload.parentId,
            Category.name == payload.name,
            Category.deletedAt.is_(None)
        )
    )
    if dupName.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Category with this name already exists under the same parent")

    # 3. Duplicate Check: Slug uniqueness for the tenant
    dupSlug = await db.execute(
        select(Category).where(
            Category.tenantId == payload.tenantId,
            Category.slug == payload.slug,
            Category.deletedAt.is_(None)
        )
    )
    if dupSlug.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Category with this slug already exists for this tenant")

    category = Category(**payload.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


# ── LIST ─────────────────────────────────────
@router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    tenantId: UUID,
    parentId: Optional[UUID] = Query(None, description="Filter by parent ID. Send 'null' or omit for top-level"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Category).where(Category.tenantId == tenantId, Category.deletedAt.is_(None))
    # Note: Query(None) can be checked. If parentId is explicitly passed or filtered
    if parentId:
        query = query.where(Category.parentId == parentId)
    else:
        # If the user wants to list all, we can allow parentId to be omitted.
        # But if they specify parentId filter, we apply it. Let's make it optional.
        pass

    result = await db.execute(query)
    return result.scalars().all()


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

    # Validate parent and cycle if parentId changes
    if "parentId" in updateData:
        newParentId = updateData["parentId"]
        if newParentId is not None:
            # Check if parent exists
            parentRes = await db.execute(
                select(Category).where(Category.id == newParentId, Category.deletedAt.is_(None))
            )
            if not parentRes.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Parent category not found")
            # Check cyclic loop
            await validate_category_hierarchy(db, categoryId, newParentId)

    # Validate duplicate name under same parent if name or parentId changes
    targetParent = updateData.get("parentId", category.parentId)
    targetName = updateData.get("name", category.name)
    if "name" in updateData or "parentId" in updateData:
        dupName = await db.execute(
            select(Category).where(
                Category.tenantId == category.tenantId,
                Category.parentId == targetParent,
                Category.name == targetName,
                Category.id != categoryId,
                Category.deletedAt.is_(None)
            )
        )
        if dupName.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Category with this name already exists under the same parent")

    # Validate duplicate slug if slug changes
    if "slug" in updateData:
        dupSlug = await db.execute(
            select(Category).where(
                Category.tenantId == category.tenantId,
                Category.slug == updateData["slug"],
                Category.id != categoryId,
                Category.deletedAt.is_(None)
            )
        )
        if dupSlug.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Category with this slug already exists for this tenant")

    for field, value in updateData.items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)
    return category


# ── DELETE ───────────────────────────────────
@router.delete("/{categoryId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(categoryId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category).where(Category.id == categoryId, Category.deletedAt.is_(None))
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.deletedAt = datetime.now(timezone.utc).replace(tzinfo=None)
    await db.commit()

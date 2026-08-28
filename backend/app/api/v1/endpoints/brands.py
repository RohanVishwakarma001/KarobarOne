# Owner - pradhansaikat123@gmail.com
# Router for brands.
# Manages CRUD operations, validation, and auto-timestamps when transitions occur.

# Import regular expressions module for parsing slug patterns
import re
# Import datetime to populate timestamps for brand approvals
from datetime import datetime
# Import List and Optional types for type annotation and query parameters
from typing import List, Optional
# Import UUID class for validating database identifiers
from uuid import UUID

# Import APIRouter, Depends injection, and HTTP exceptions from FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
# Import select to construct query statements
from sqlalchemy import select
# Import IntegrityError to catch database unique/integrity constraints on commit
from sqlalchemy.exc import IntegrityError
# Import AsyncSession for managing asynchronous database transactions
from sqlalchemy.ext.asyncio import AsyncSession

# Import get_db dependency helper to obtain the active async database session
from app.db.session import getDb
# Import Brand model class to represent the brands database table
from app.db.models.brands import Brand
# Import Pydantic schemas for request validation and structured response output
from app.schemas.brands import BrandCreate, BrandResponse, BrandUpdate

router = APIRouter(prefix="/brands", tags=["Brands"])


def slugify(s: str) -> str:
    # Convert to lower case, replace non-alphanumeric/spaces with empty,
    # and replace spaces/hyphens with a single hyphen.
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return s.strip("-")


@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def createBrand(payload: BrandCreate, db: AsyncSession = Depends(getDb)):
    data = payload.model_dump()
    
    # Auto-generate brandSlug if not provided
    if not data.get("brandSlug"):
        data["brandSlug"] = slugify(data["brandName"])
        
    dbBrand = Brand(**data)
    
    try:
        db.add(dbBrand)
        await db.commit()
        await db.refresh(dbBrand)
        return dbBrand
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brand slug or owner store brand name combination already exists."
        )


@router.get("/", response_model=List[BrandResponse])
async def listBrands(
    tenantId: Optional[UUID] = None,
    ownerStoreId: Optional[UUID] = None,
    verificationStatus: Optional[str] = None,
    isPlatformBrand: Optional[bool] = None,
    isActive: Optional[bool] = None,
    isRaw: bool = False,  # If True, returns soft-deleted brands too
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(getDb),
):
    query = select(Brand)
    
    if tenantId:
        query = query.where(Brand.tenantId == tenantId)
    if ownerStoreId:
        query = query.where(Brand.ownerStoreId == ownerStoreId)
    if verificationStatus:
        query = query.where(Brand.verificationStatus == verificationStatus)
    if isPlatformBrand is not None:
        query = query.where(Brand.isPlatformBrand == isPlatformBrand)
    if isActive is not None:
        query = query.where(Brand.isActive == isActive)
    
    # By default, exclude soft-deleted records
    if not isRaw:
        query = query.where(Brand.deletedAt.is_(None))
        
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{brandId}", response_model=BrandResponse)
async def getBrand(brandId: UUID, isRaw: bool = False, db: AsyncSession = Depends(getDb)):
    query = select(Brand).where(Brand.id == brandId)
    if not isRaw:
        query = query.where(Brand.deletedAt.is_(None))
        
    result = await db.execute(query)
    dbBrand = result.scalar_one_or_none()
    
    if not dbBrand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found or has been deleted."
        )
    return dbBrand


@router.patch("/{brandId}", response_model=BrandResponse)
async def updateBrand(
    brandId: UUID, payload: BrandUpdate, db: AsyncSession = Depends(getDb)
):
    result = await db.execute(select(Brand).where(Brand.id == brandId).where(Brand.deletedAt.is_(None)))
    dbBrand = result.scalar_one_or_none()
    
    if not dbBrand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found or has been deleted."
        )
        
    updateData = payload.model_dump(exclude_none=True)
    
    # If brandSlug is explicitly updated, make sure it is slugified
    if "brandSlug" in updateData:
        updateData["brandSlug"] = slugify(updateData["brandSlug"])
        
    # Auto-update approved_at and approved_by if verificationStatus is changed to APPROVED
    if "verificationStatus" in updateData:
        if updateData["verificationStatus"] == "APPROVED":
            dbBrand.approvedAt = datetime.now()
            # If approvedBy is updated or we use the creator/reviewer UUID
            # (allow setting via query or default to a dummy/provided value if available)
        elif updateData["verificationStatus"] in {"PENDING", "REJECTED"}:
            dbBrand.approvedAt = None
            dbBrand.approvedBy = None

    for field, value in updateData.items():
        setattr(dbBrand, field, value)
        
    try:
        await db.commit()
        await db.refresh(dbBrand)
        return dbBrand
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Updating this brand creates a unique constraint conflict (duplicate brand slug or owner store brand name)."
        )


@router.delete("/{brandId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteBrand(brandId: UUID, db: AsyncSession = Depends(getDb)):
    result = await db.execute(select(Brand).where(Brand.id == brandId).where(Brand.deletedAt.is_(None)))
    dbBrand = result.scalar_one_or_none()
    
    if not dbBrand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found or has already been deleted."
        )
        
    # Soft delete
    dbBrand.deletedAt = datetime.now()
    dbBrand.isActive = False
    
    await db.commit()


@router.get("/trash/list", response_model=List[BrandResponse])
async def listTrashBrands(db: AsyncSession = Depends(getDb)):
    result = await db.execute(select(Brand).where(Brand.deletedAt.is_not(None)))
    return result.scalars().all()


@router.post("/{brandId}/restore", response_model=BrandResponse)
async def restoreBrand(brandId: UUID, db: AsyncSession = Depends(getDb)):
    result = await db.execute(select(Brand).where(Brand.id == brandId).where(Brand.deletedAt.is_not(None)))
    dbBrand = result.scalar_one_or_none()
    if not dbBrand:
        raise HTTPException(status_code=404, detail="Deleted brand not found")
    
    dbBrand.deletedAt = None
    dbBrand.isActive = True
    await db.commit()
    await db.refresh(dbBrand)
    return dbBrand


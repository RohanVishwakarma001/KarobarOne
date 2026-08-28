# Owner - pradhansaikat123@gmail.com

# Variants API endpoints. Supports CRUD, SKU uniqueness, and 
# duplicate attribute combination validation.

# Import List and Optional from typing for type declarations
from typing import List, Optional
# Import UUID from uuid for unique identifier support
from uuid import UUID
# Import datetime and timezone from datetime for handling dates
from datetime import datetime, timezone

# Import APIRouter, Depends, HTTPException, and status from fastapi
from fastapi import APIRouter, Depends, HTTPException, status
# Import select from sqlalchemy for database queries
from sqlalchemy import select
# Import AsyncSession from sqlalchemy.ext.asyncio for asynchronous sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import get_db session dependency injection helper
from app.productsPorted.core.database import get_db
# Import Variant and Product models from models
from app.productsPorted.models.models import Variant, Product
# Import schemas from schemas
from app.productsPorted.schemas.schemas import VariantCreate, VariantResponse, VariantUpdate

router = APIRouter(prefix="/variants", tags=["Products - Variants"])


def attributeCombinationsEqual(dict1, dict2) -> bool:
    """Helper to check if two attribute dictionaries are equal, ignoring ordering."""
    if not dict1 and not dict2:
        return True
    if not dict1 or not dict2:
        return False
    return dict1 == dict2


async def validate_variant_attributes(db: AsyncSession, productId: UUID, attributes: Optional[dict], excludeVariantId: Optional[UUID] = None):
    """
    Validates that no other variant for the given product has the exact same combination of attributes.
    """
    stmt = select(Variant).where(
        Variant.productId == productId
    )
    if excludeVariantId:
        stmt = stmt.where(Variant.id != excludeVariantId)
        
    res = await db.execute(stmt)
    existingVariants = res.scalars().all()

    for var in existingVariants:
        if attributeCombinationsEqual(var.attributes, attributes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A variant with this exact combination of attributes already exists for this product."
            )


# ── CREATE VARIANT ───────────────────────────
@router.post("/", response_model=VariantResponse, status_code=status.HTTP_201_CREATED)
async def create_variant(payload: VariantCreate, db: AsyncSession = Depends(get_db)):
    # 1. Verify product exists
    prodRes = await db.execute(
        select(Product).where(Product.id == payload.productId, Product.deletedAt.is_(None))
    )
    if not prodRes.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Duplicate Check: SKU under the same product
    skuRes = await db.execute(
        select(Variant).where(
            Variant.productId == payload.productId,
            Variant.sku == payload.sku
        )
    )
    if skuRes.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Variant with this SKU already exists for this product")

    # 3. Duplicate Check: Attribute combination
    await validate_variant_attributes(db, payload.productId, payload.attributes)

    variant = Variant(**payload.model_dump())
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    return variant


# ── LIST VARIANTS FOR PRODUCT ────────────────
@router.get("/", response_model=List[VariantResponse])
async def list_variants(productId: UUID, db: AsyncSession = Depends(get_db)):
    # Verify product exists
    prodRes = await db.execute(
        select(Product).where(Product.id == productId, Product.deletedAt.is_(None))
    )
    if not prodRes.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    res = await db.execute(
        select(Variant).where(Variant.productId == productId)
    )
    return res.scalars().all()


# ── GET VARIANT BY ID ────────────────────────
@router.get("/{variantId}", response_model=VariantResponse)
async def get_variant(variantId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Variant).where(Variant.id == variantId)
    )
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant


# ── UPDATE VARIANT ───────────────────────────
@router.patch("/{variantId}", response_model=VariantResponse)
async def update_variant(
    variantId: UUID, payload: VariantUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Variant).where(Variant.id == variantId)
    )
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    updateData = payload.model_dump(exclude_none=True)

    if "sku" in updateData:
        # Check duplicate SKU
        skuRes = await db.execute(
            select(Variant).where(
                Variant.productId == variant.productId,
                Variant.sku == updateData["sku"],
                Variant.id != variantId
            )
        )
        if skuRes.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Variant with this SKU already exists")

    if "attributes" in updateData:
        # Check duplicate attribute combination
        await validate_variant_attributes(
            db=db,
            productId=variant.productId,
            attributes=updateData["attributes"],
            excludeVariantId=variantId
        )

    for field, value in updateData.items():
        setattr(variant, field, value)

    await db.commit()
    await db.refresh(variant)
    return variant


# ── DELETE VARIANT ───────────────────────────
@router.delete("/{variantId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(variantId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Variant).where(Variant.id == variantId)
    )
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    await db.delete(variant)
    await db.commit()

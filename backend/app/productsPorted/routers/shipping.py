# Owner - pradhansaikat123@gmail.com

# Shipping Profiles API endpoints. Supports CRUD for shipping rules,
# including delivery estimates and charges.

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
# Import ShippingProfile model from models
from app.productsPorted.models.models import ShippingProfile
# Import schemas from app schemas
from app.productsPorted.schemas.schemas import ShippingProfileCreate, ShippingProfileResponse, ShippingProfileUpdate

router = APIRouter(prefix="/shipping", tags=["Products - Shipping"])


# ── CREATE ───────────────────────────────────
@router.post("/", response_model=ShippingProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_shipping_profile(payload: ShippingProfileCreate, db: AsyncSession = Depends(get_db)):
    # Duplicate check: tenantId + name
    dup = await db.execute(
        select(ShippingProfile).where(
            ShippingProfile.tenantId == payload.tenantId,
            ShippingProfile.name == payload.name,
            ShippingProfile.isActive == True
        )
    )
    if dup.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Shipping profile with this name already exists for this tenant")

    profile = ShippingProfile(**payload.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


# ── LIST ─────────────────────────────────────
@router.get("/", response_model=List[ShippingProfileResponse])
async def list_shipping_profiles(tenantId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ShippingProfile).where(
            ShippingProfile.tenantId == tenantId,
            ShippingProfile.isActive == True
        )
    )
    return result.scalars().all()


# ── GET BY ID ────────────────────────────────
@router.get("/{profileId}", response_model=ShippingProfileResponse)
async def get_shipping_profile(profileId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ShippingProfile).where(
            ShippingProfile.id == profileId,
            ShippingProfile.isActive == True
        )
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Shipping profile not found")
    return profile


# ── UPDATE ───────────────────────────────────
@router.patch("/{profileId}", response_model=ShippingProfileResponse)
async def update_shipping_profile(
    profileId: UUID, payload: ShippingProfileUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ShippingProfile).where(
            ShippingProfile.id == profileId,
            ShippingProfile.isActive == True
        )
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Shipping profile not found")

    updateData = payload.model_dump(exclude_none=True)

    if "name" in updateData:
        dup = await db.execute(
            select(ShippingProfile).where(
                ShippingProfile.tenantId == profile.tenantId,
                ShippingProfile.name == updateData["name"],
                ShippingProfile.id != profileId,
                ShippingProfile.isActive == True
            )
        )
        if dup.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Shipping profile with this name already exists")

    for field, value in updateData.items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)
    return profile


# ── DELETE ───────────────────────────────────
@router.delete("/{profileId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipping_profile(profileId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ShippingProfile).where(
            ShippingProfile.id == profileId,
            ShippingProfile.isActive == True
        )
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Shipping profile not found")

    profile.isActive = False
    await db.commit()

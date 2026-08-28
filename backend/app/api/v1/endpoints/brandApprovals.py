# Owner - pradhansaikat123@gmail.com
# Router for brand approvals.
# Manages CRUD operations, validation, and auto-timestamps when transitions occur.

# Import datetime to manage review and revocation timestamps
from datetime import datetime
# Import List and Optional types for data structures and optional query filters
from typing import List, Optional
# Import UUID class for validated database and route identifiers
from uuid import UUID

# Import APIRouter, Depends injection, and HTTP exception components from FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
# Import select to construct database queries
from sqlalchemy import select
# Import IntegrityError to catch and handle database constraint violations
from sqlalchemy.exc import IntegrityError
# Import AsyncSession for managing asynchronous database transactions
from sqlalchemy.ext.asyncio import AsyncSession

# Import get_db dependency to supply active async database sessions
from app.db.session import getDb
# Import Brand and BrandApproval model classes to interact with the database tables
from app.db.models.brands import Brand, BrandApproval
# Import Pydantic schemas for request validation and structured response output
from app.schemas.brands import BrandApprovalCreate, BrandApprovalResponse, BrandApprovalUpdate

router = APIRouter(prefix="/brand-approvals", tags=["Brand Approvals"])


@router.post("/", response_model=BrandApprovalResponse, status_code=status.HTTP_201_CREATED)
async def createBrandApproval(
    payload: BrandApprovalCreate, db: AsyncSession = Depends(getDb)
):
    # Verify the target brand exists
    brandCheck = await db.execute(select(Brand).where(Brand.id == payload.brandId).where(Brand.deletedAt.is_(None)))
    dbBrand = brandCheck.scalar_one_or_none()
    if not dbBrand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found or has been deleted."
        )

    # Perform runtime constraint validation matching database CHECKs
    if payload.requestingStoreId == payload.brandOwnerStoreId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="requestingStoreId cannot be the same as brandOwnerStoreId."
        )

    if payload.approvalStartDate and payload.approvalEndDate:
        if payload.approvalStartDate > payload.approvalEndDate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="approvalStartDate must be less than or equal to approvalEndDate."
            )

    dbApproval = BrandApproval(**payload.model_dump())
    
    try:
        db.add(dbApproval)
        await db.commit()
        await db.refresh(dbApproval)
        return dbApproval
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An approval request for this brand by this requesting store already exists."
        )


@router.get("/", response_model=List[BrandApprovalResponse])
async def listBrandApprovals(
    brandId: Optional[UUID] = None,
    requestingStoreId: Optional[UUID] = None,
    brandOwnerStoreId: Optional[UUID] = None,
    requestStatus: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(getDb),
):
    query = select(BrandApproval)
    
    if brandId:
        query = query.where(BrandApproval.brandId == brandId)
    if requestingStoreId:
        query = query.where(BrandApproval.requestingStoreId == requestingStoreId)
    if brandOwnerStoreId:
        query = query.where(BrandApproval.brandOwnerStoreId == brandOwnerStoreId)
    if requestStatus:
        query = query.where(BrandApproval.requestStatus == requestStatus)
        
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{approvalId}", response_model=BrandApprovalResponse)
async def getBrandApproval(approvalId: UUID, db: AsyncSession = Depends(getDb)):
    result = await db.execute(select(BrandApproval).where(BrandApproval.id == approvalId))
    dbApproval = result.scalar_one_or_none()
    
    if not dbApproval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand approval request not found."
        )
    return dbApproval


@router.patch("/{approvalId}", response_model=BrandApprovalResponse)
async def updateBrandApproval(
    approvalId: UUID, payload: BrandApprovalUpdate, db: AsyncSession = Depends(getDb)
):
    result = await db.execute(select(BrandApproval).where(BrandApproval.id == approvalId))
    dbApproval = result.scalar_one_or_none()
    
    if not dbApproval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand approval request not found."
        )
        
    updateData = payload.model_dump(exclude_none=True)
    
    # Auto-populate transition timestamps based on status updates
    if "requestStatus" in updateData:
        statusVal = updateData["requestStatus"]
        if statusVal in {"APPROVED", "REJECTED"}:
            dbApproval.reviewedAt = datetime.now()
            # If reviewedBy is not explicitly supplied, let it remain or set if provided
        elif statusVal == "REVOKED":
            dbApproval.revokedAt = datetime.now()
            # If revokedBy is not explicitly supplied, let it remain or set if provided
        elif statusVal == "PENDING":
            dbApproval.reviewedAt = None
            dbApproval.reviewedBy = None
            dbApproval.revokedAt = None
            dbApproval.revokedBy = None

    for field, value in updateData.items():
        setattr(dbApproval, field, value)
        
    # Re-validate date range constraints if start/end dates are updated
    if dbApproval.approvalStartDate and dbApproval.approvalEndDate:
        if dbApproval.approvalStartDate > dbApproval.approvalEndDate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="approvalStartDate must be less than or equal to approvalEndDate."
            )
            
    try:
        await db.commit()
        await db.refresh(dbApproval)
        return dbApproval
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Updating this request conflicts with a unique constraint or check constraint."
        )


@router.delete("/{approvalId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteBrandApproval(approvalId: UUID, db: AsyncSession = Depends(getDb)):
    result = await db.execute(select(BrandApproval).where(BrandApproval.id == approvalId))
    dbApproval = result.scalar_one_or_none()
    
    if not dbApproval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand approval request not found."
        )
        
    await db.delete(dbApproval)
    await db.commit()

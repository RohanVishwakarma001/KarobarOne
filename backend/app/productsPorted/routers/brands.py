# Owner - pradhansaikat123@gmail.com

# Brands and Brand Approval API endpoints. Supports CRUD for brands,
# submitting brand authorization requests, approving/rejecting requests,
# and writing to the audit logs.

# Import uuid module for unique ID generation
import uuid
# Import List and Optional from typing for type hints
from typing import List, Optional
# Import UUID from uuid for unique identifiers
from uuid import UUID
# Import datetime and timezone from datetime for datetime logic
from datetime import datetime, timezone

# Import APIRouter, Depends, HTTPException, and status from fastapi
from fastapi import APIRouter, Depends, HTTPException, status
# Import select from sqlalchemy for database queries
from sqlalchemy import select
# Import AsyncSession from sqlalchemy.ext.asyncio for database connection sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import get_db session dependency injection helper
from app.productsPorted.core.database import get_db
# Import Brand, BrandApprovalRequest, BrandApprovalAuditLog models
from app.productsPorted.models.models import Brand, BrandApprovalRequest, BrandApprovalAuditLog
# Import schemas from app schemas
from app.productsPorted.schemas.schemas import (
    BrandCreate,
    BrandResponse,
    BrandUpdate,
    BrandApprovalRequestResponse,
    BrandApprovalDecision,
    BrandApprovalAuditLogResponse,
    BrandApprovalRequestCreate
)

router = APIRouter(prefix="/brands", tags=["Products - Brands & Approvals"])


# ── CREATE BRAND ─────────────────────────────
@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(payload: BrandCreate, db: AsyncSession = Depends(get_db)):
    # Duplicate check: tenantId + name
    dup = await db.execute(
        select(Brand).where(
            Brand.tenantId == payload.tenantId,
            Brand.name == payload.name,
            Brand.deletedAt.is_(None)
        )
    )
    if dup.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Brand with this name already exists for this tenant")

    brand = Brand(**payload.model_dump())
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand


# ── LIST BRANDS ──────────────────────────────
@router.get("/", response_model=List[BrandResponse])
async def list_brands(tenantId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Brand).where(
            Brand.tenantId == tenantId,
            Brand.deletedAt.is_(None)
        )
    )
    return result.scalars().all()


# ── GET BRAND BY ID ──────────────────────────
@router.get("/{brandId}", response_model=BrandResponse)
async def get_brand(brandId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Brand).where(
            Brand.id == brandId,
            Brand.deletedAt.is_(None)
        )
    )
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


# ── UPDATE BRAND ─────────────────────────────
@router.patch("/{brandId}", response_model=BrandResponse)
async def update_brand(
    brandId: UUID, payload: BrandUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Brand).where(
            Brand.id == brandId,
            Brand.deletedAt.is_(None)
        )
    )
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    updateData = payload.model_dump(exclude_none=True)

    if "name" in updateData:
        dup = await db.execute(
            select(Brand).where(
                Brand.tenantId == brand.tenantId,
                Brand.name == updateData["name"],
                Brand.id != brandId,
                Brand.deletedAt.is_(None)
            )
        )
        if dup.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Brand with this name already exists")

    for field, value in updateData.items():
        setattr(brand, field, value)

    await db.commit()
    await db.refresh(brand)
    return brand


# ── DELETE BRAND ─────────────────────────────
@router.delete("/{brandId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(brandId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Brand).where(
            Brand.id == brandId,
            Brand.deletedAt.is_(None)
        )
    )
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    brand.deletedAt = datetime.now(timezone.utc).replace(tzinfo=None)
    await db.commit()


# ── SUBMIT APPROVAL REQUEST ──────────────────
@router.post("/{brandId}/request-approval", response_model=BrandApprovalRequestResponse, status_code=status.HTTP_201_CREATED)
async def request_approval(
    brandId: UUID, payload: BrandApprovalRequestCreate, db: AsyncSession = Depends(get_db)
):
    # Verify brand exists
    brandRes = await db.execute(
        select(Brand).where(Brand.id == brandId, Brand.deletedAt.is_(None))
    )
    brand = brandRes.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Check if there is already an active pending approval request
    existingReq = await db.execute(
        select(BrandApprovalRequest).where(
            BrandApprovalRequest.brandId == brandId,
            BrandApprovalRequest.status == "PENDING"
        )
    )
    if existingReq.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="There is already a pending approval request for this brand")

    # Create approval request
    request = BrandApprovalRequest(
        brandId=brandId,
        requestedBy=payload.requestedBy,
        brandOwnerStoreId=brand.ownerStoreId or payload.requestedBy or uuid.uuid4(),
        status="PENDING"
    )
    db.add(request)
    await db.flush()  # to get request.id

    # Add audit log (SQLite only)
    if db.bind.dialect.name == "sqlite":
        auditLog = BrandApprovalAuditLog(
            brandId=brandId,
            requestId=request.id,
            action="SUBMIT",
            performedBy=payload.requestedBy,
            notes="Brand authorization requested."
        )
        db.add(auditLog)
    await db.commit()
    await db.refresh(request)
    return request


# ── APPROVE BRAND ────────────────────────────
@router.post("/{brandId}/approve", response_model=BrandResponse)
async def approve_brand(
    brandId: UUID, payload: BrandApprovalDecision, db: AsyncSession = Depends(get_db)
):
    # Verify brand exists
    brandRes = await db.execute(
        select(Brand).where(Brand.id == brandId, Brand.deletedAt.is_(None))
    )
    brand = brandRes.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Find the active pending request
    reqRes = await db.execute(
        select(BrandApprovalRequest).where(
            BrandApprovalRequest.brandId == brandId,
            BrandApprovalRequest.status == "PENDING"
        )
    )
    request = reqRes.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=400, detail="No pending approval request found for this brand")

    # Update request
    request.status = "APPROVED"
    
    # Update brand
    brand.isApproved = True
    brand.approvedBy = payload.performedBy
    brand.approvedAt = datetime.now(timezone.utc).replace(tzinfo=None)

    # Audit log (SQLite only)
    if db.bind.dialect.name == "sqlite":
        auditLog = BrandApprovalAuditLog(
            brandId=brandId,
            requestId=request.id,
            action="APPROVE",
            performedBy=payload.performedBy,
            notes=payload.notes or "Brand approved by owner."
        )
        db.add(auditLog)
    await db.commit()
    await db.refresh(brand)
    return brand


# ── REJECT BRAND ────────────────────────────
@router.post("/{brandId}/reject", response_model=BrandResponse)
async def reject_brand(
    brandId: UUID, payload: BrandApprovalDecision, db: AsyncSession = Depends(get_db)
):
    # Verify brand exists
    brandRes = await db.execute(
        select(Brand).where(Brand.id == brandId, Brand.deletedAt.is_(None))
    )
    brand = brandRes.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Find the active pending request
    reqRes = await db.execute(
        select(BrandApprovalRequest).where(
            BrandApprovalRequest.brandId == brandId,
            BrandApprovalRequest.status == "PENDING"
        )
    )
    request = reqRes.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=400, detail="No pending approval request found for this brand")

    # Update request
    request.status = "REJECTED"
    request.rejectionReason = payload.rejectionReason or "No reason provided."
    
    # Update brand
    brand.isApproved = False
    brand.approvedBy = None
    brand.approvedAt = None

    # Audit log (SQLite only)
    if db.bind.dialect.name == "sqlite":
        auditLog = BrandApprovalAuditLog(
            brandId=brandId,
            requestId=request.id,
            action="REJECT",
            performedBy=payload.performedBy,
            notes=f"Brand rejected: {payload.rejectionReason or 'No reason provided.'}"
        )
        db.add(auditLog)
    await db.commit()
    await db.refresh(brand)
    return brand


# ── AUDIT LOGS FOR BRAND ─────────────────────
@router.get("/{brandId}/audit-logs", response_model=List[BrandApprovalAuditLogResponse])
async def list_audit_logs(brandId: UUID, db: AsyncSession = Depends(get_db)):
    if db.bind.dialect.name == "sqlite":
        res = await db.execute(
            select(BrandApprovalAuditLog).where(BrandApprovalAuditLog.brandId == brandId).order_by(BrandApprovalAuditLog.createdAt.desc())
        )
        return res.scalars().all()
    else:
        # Dynamically construct audit logs from the request records on PostgreSQL
        res = await db.execute(
            select(BrandApprovalRequest).where(BrandApprovalRequest.brandId == brandId).order_by(BrandApprovalRequest.createdAt.desc())
        )
        requests = res.scalars().all()
        auditLogs = []
        for req in requests:
            auditLogs.append({
                "id": req.id,
                "brandId": req.brandId,
                "requestId": req.id,
                "action": "SUBMIT",
                "performedBy": req.requestedBy,
                "notes": "Brand authorization requested.",
                "createdAt": req.createdAt
            })
            if req.status in ("APPROVED", "REJECTED"):
                auditLogs.append({
                    "id": req.id,
                    "brandId": req.brandId,
                    "requestId": req.id,
                    "action": "APPROVE" if req.status == "APPROVED" else "REJECT",
                    "performedBy": req.requestedBy,
                    "notes": req.rejectionReason or "Brand decision processed.",
                    "createdAt": req.updatedAt
                })
        return sorted(auditLogs, key=lambda x: x["createdAt"], reverse=True)

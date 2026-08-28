# Owner - pradhansaikat123@gmail.com
# ================================================================================
# FILE: api/v1/endpoints/approvalRequests.py — Approval Request Endpoints
# ================================================================================
# Why this file is used:
#   - Exposes API endpoints for managing the approval lifecycle (draft, submit,
#     update, withdraw, approve, reject).
#
# What components are inside:
#   - APIRouter         -> Mounted under /approval-requests
#   - POST /draft       -> Save changes as a draft version (unpublished)
#   - POST /submit      -> Submit change request for review
#   - PUT /{id}/draft   -> Modify a PENDING request's data
#   - POST /{id}/withdraw -> Cancel a PENDING request
#   - POST /{id}/approve -> Approve request & trigger publishing
#   - POST /{id}/reject  -> Reject request with mandatory reason
#   - Standard CRUD (list, get, delete) preserved for fallback
# ================================================================================
"""
Endpoints for approval requests lifecycle management.
Integrates directly with ApprovalService.
"""

# Import List and Optional types for annotations
from typing import List, Optional
# Import UUID class for typing unique database identifiers
from uuid import UUID
# Import FastAPI components for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import AsyncSession for database operations
from sqlalchemy.ext.asyncio import AsyncSession

# Import DB session provider dependency
from app.db.session import getDb as get_db
# Import ApprovalRequest and ApprovalRequestVersion models
from app.db.models.approvals import ApprovalRequest, ApprovalRequestVersion

# owner: mousamdas156@gmail.com
# Import Pydantic schemas for input validation and structured response output
from app.schemas.approvals import (
    ApprovalRequestCreate,
    ApprovalRequestResponse,
    ApprovalRequestUpdate,
    ApprovalRequestVersionCreate,
    ApprovalRequestVersionResponse,
    ApprovalRequestVersionUpdate,
    DraftCreate,
    RequestSubmit,
    DraftUpdate,
    ApprovePayload,
    RejectPayload,
    EntityVersionResponse,
)
# Import central ApprovalService
from app.services.approvalService import ApprovalService
# Import exception mapping classes
from app.core.exceptionsCompat import NotFoundError, ConflictError, BusinessValidationError

router = APIRouter(prefix="/approval-requests", tags=["Approval Requests"])


# ═══════════════════════════════════════════════
# NEW WORKFLOW ENDPOINTS (Stories 1, 3, 4)
# owner: mousamdas156@gmail.com
# ═══════════════════════════════════════════════

@router.post("/draft", response_model=EntityVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_draft(
    payload: DraftCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Saves entity changes as a draft version (isPublished=False) without submitting for review.
    """
    service = ApprovalService(db)
    try:
        draft = await service.createDraft(
            tenantId=payload.tenantId,
            entityType=payload.entityType,
            entityId=payload.entityId,
            versionData=payload.versionData,
            createdBy=payload.createdBy,
        )
        return draft
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/submit", response_model=ApprovalRequestResponse, status_code=status.HTTP_201_CREATED)
async def submit_request(
    payload: RequestSubmit,
    db: AsyncSession = Depends(get_db),
):
    """
    Submits a change request for review. Generates an EntityVersion and seeds the Review Queue.
    """
    service = ApprovalService(db)
    try:
        request = await service.submitForApproval(
            tenantId=payload.tenantId,
            entityType=payload.entityType,
            entityId=payload.entityId,
            operationType=payload.operationType,
            versionData=payload.versionData,
            submittedBy=payload.submittedBy,
            remarks=payload.remarks,
        )
        return request
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{requestId}/draft", response_model=EntityVersionResponse)
async def update_pending_draft(
    requestId: UUID,
    payload: DraftUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Modifies the entity data snapshot of a change request.
    Only permitted if the request status is still PENDING.
    """
    service = ApprovalService(db)
    try:
        updated_draft = await service.updatePendingDraft(
            requestId=requestId,
            versionData=payload.versionData,
        )
        return updated_draft
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


@router.post("/{requestId}/withdraw", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_request(
    requestId: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Withdraws (cancels) a pending approval request. Removes review queue entry.
    Only permitted if the request status is still PENDING.
    """
    service = ApprovalService(db)
    try:
        await service.withdrawRequest(requestId)
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


@router.post("/{requestId}/approve", response_model=ApprovalRequestResponse)
async def approve_request(
    requestId: UUID,
    payload: ApprovePayload,
    db: AsyncSession = Depends(get_db),
):
    """
    Approves a request, applying version data to the live table via Publishing Engine.
    """
    service = ApprovalService(db)
    try:
        approved_request = await service.approveRequest(
            requestId=requestId,
            reviewedBy=payload.reviewedBy,
            remarks=payload.remarks,
        )
        return approved_request
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


@router.post("/{requestId}/reject", response_model=ApprovalRequestResponse)
async def reject_request(
    requestId: UUID,
    payload: RejectPayload,
    db: AsyncSession = Depends(get_db),
):
    """
    Rejects a request with a mandatory rejection reason. Generates notification event.
    """
    service = ApprovalService(db)
    try:
        rejected_request = await service.rejectRequest(
            requestId=requestId,
            reviewedBy=payload.reviewedBy,
            rejectionReason=payload.rejectionReason,
            remarks=payload.remarks,
        )
        return rejected_request
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


# ═══════════════════════════════════════════════
# STANDARD CRUD FALLBACKS
# ═══════════════════════════════════════════════

@router.get("/", response_model=List[ApprovalRequestResponse])
async def list_approval_requests(
    tenantId: Optional[UUID] = None,
    entityType: Optional[str] = None,
    entityId: Optional[UUID] = None,
    approvalStatus: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    Lists approval requests with filtering and pagination.
    """
    query = select(ApprovalRequest)
    if tenantId:
        query = query.where(ApprovalRequest.tenantId == tenantId)
    if entityType:
        query = query.where(ApprovalRequest.entityType == entityType)
    if entityId:
        query = query.where(ApprovalRequest.entityId == entityId)
    if approvalStatus:
        query = query.where(ApprovalRequest.approvalStatus == approvalStatus)

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{requestId}", response_model=ApprovalRequestResponse)
async def get_approval_request(
    requestId: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a single approval request detail.
    """
    result = await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == requestId))
    dbRequest = result.scalar_one_or_none()
    if not dbRequest:
        raise HTTPException(status_code=404, detail="Approval request not found")
    return dbRequest


@router.delete("/{requestId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_approval_request(
    requestId: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Hard delete an approval request.
    """
    result = await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == requestId))
    dbRequest = result.scalar_one_or_none()
    if not dbRequest:
        raise HTTPException(status_code=404, detail="Approval request not found")
    await db.delete(dbRequest)
    await db.commit()

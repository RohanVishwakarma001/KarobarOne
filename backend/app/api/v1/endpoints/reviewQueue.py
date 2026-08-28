# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: api/v1/endpoints/reviewQueue.py — Review Queue Endpoints
# ================================================================================
# Why this file is used:
#   - Exposes REST API endpoints for platform staff to fetch, prioritize, filter,
#     and assign requests from the review queue.
#
# What components are inside:
#   - GET /             -> List queue items with joined filters and sorting
#   - GET /{queueId}    -> Get a single queue item with details
#   - PATCH /{queueId}/assign -> Assign a queue item to platform staff
# ================================================================================
"""
Endpoints for Review Queue management.
"""

# Import List and Optional typing helpers for query params
from typing import List, Optional
# Import UUID class for typing ID path parameters
from uuid import UUID
# Import FastAPI components for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
# Import AsyncSession for database operations context
from sqlalchemy.ext.asyncio import AsyncSession

# Import database session provider
from app.db.session import getDb as get_db
# Import ReviewQueue DB model
from app.db.models.approvals import ReviewQueue
# Import ReviewQueue repository
from app.repositories.reviewQueueRepository import ReviewQueueRepository
# Import request and response validation schemas
from app.schemas.approvals import ReviewQueueResponse, ReviewQueueAssign
# Import custom exception wrappers
from app.core.exceptionsCompat import NotFoundError

router = APIRouter(prefix="/review-queue", tags=["Review Queue"])


@router.get("/", response_model=List[ReviewQueueResponse])
async def list_review_queue(
    tenantId: Optional[UUID] = None,
    entityType: Optional[str] = None,
    approvalStatus: Optional[str] = None,
    assignedTo: Optional[UUID] = None,
    sortBy: str = "date",
    sortOrder: str = "desc",
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    What it does:
        Fetches a list of ReviewQueue entries matching query filters for tenant,
        entityType, approvalStatus, and assignment. Applies priority/date sorting.
    Why it is used:
        Allows platform staff to browse, search, and prioritize pending items
        inside the dashboard review panel.
    """
    repo = ReviewQueueRepository(ReviewQueue, db)
    items, _ = await repo.listWithFilters(
        tenantId=tenantId,
        entityType=entityType,
        approvalStatus=approvalStatus,
        assignedTo=assignedTo,
        sortBy=sortBy,
        sortOrder=sortOrder,
        skip=offset,
        limit=limit,
    )
    return items


@router.get("/{queueId}", response_model=ReviewQueueResponse)
async def get_queue_item(
    queueId: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    What it does:
        Retrieves details of a single ReviewQueue entry by its UUID primary key.
    Why it is used:
        Used by review queue views to load deep information for a specific item
        when displaying details to a reviewer.
    """
    repo = ReviewQueueRepository(ReviewQueue, db)
    item = await repo.getById(queueId)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review queue item with id '{queueId}' not found"
        )
    return item


@router.patch("/{queueId}/assign", response_model=ReviewQueueResponse)
async def assign_queue_item(
    queueId: UUID,
    payload: ReviewQueueAssign,
    db: AsyncSession = Depends(get_db),
):
    """
    What it does:
        Updates the assignedTo user ID of a ReviewQueue item.
    Why it is used:
        Allows platform managers to assign specific change request tasks to staff members,
        delegating review responsibilities.
    """
    repo = ReviewQueueRepository(ReviewQueue, db)
    item = await repo.getById(queueId)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review queue item with id '{queueId}' not found"
        )

    updated_item = await repo.update(item, {"assignedTo": payload.assignedTo})
    return updated_item


from pydantic import BaseModel

class BulkReviewActionRequest(BaseModel):
    requestIds: List[UUID]
    action: str  # "APPROVE" or "REJECT"
    reviewedBy: UUID
    rejectionReason: Optional[str] = None
    remarks: Optional[str] = None


@router.post("/bulk-action")
async def bulk_review_action(
    payload: BulkReviewActionRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Perform bulk approval or rejection on multiple change requests simultaneously (TC-0094).
    """
    from app.services.approvalService import ApprovalService

    service = ApprovalService(db)
    results = []

    for req_id in payload.requestIds:
        try:
            if payload.action.upper() == "APPROVE":
                res = await service.approveRequest(
                    requestId=req_id,
                    reviewedBy=payload.reviewedBy,
                    remarks=payload.remarks,
                )
                results.append({"requestId": str(req_id), "status": "APPROVED"})
            elif payload.action.upper() == "REJECT":
                res = await service.rejectRequest(
                    requestId=req_id,
                    reviewedBy=payload.reviewedBy,
                    rejectionReason=payload.rejectionReason or "Bulk rejected",
                    remarks=payload.remarks,
                )
                results.append({"requestId": str(req_id), "status": "REJECTED"})
            else:
                results.append({"requestId": str(req_id), "status": "FAILED", "error": "Invalid action"})
        except Exception as e:
            results.append({"requestId": str(req_id), "status": "FAILED", "error": str(e)})

    return {"processed": len(results), "details": results}

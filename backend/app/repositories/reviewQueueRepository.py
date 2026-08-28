# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: repositories/reviewQueueRepository.py — Repository for Review Queue
# ================================================================================
# Why this file is used:
#   - Encapsulates database queries for review assignments, sorting, and filtering.
#   - Provides custom SQL expressions (like CASE sorting mapping) to order queue items
#     by priority levels.
#
# What components are inside:
#   - ReviewQueueRepository:
#       - getByApprovalRequestId() -> Lookup by approvalRequestId
#       - listWithFilters()         -> Rich dynamic filtering and sorting of queue
# ================================================================================
"""
Repository layer for ReviewQueue queries with complex joined filtering and custom sorting.
"""

# Import standard uuid class for validating unique database identifiers
import uuid
# Import Sequence and Optional typings for method signatures
from typing import Optional, Sequence
# Import select query builder, count functions, case expressions, and sort order parameters
from sqlalchemy import select, func, case, desc, asc
# Import joinedload for eager loading ApprovalRequest data
from sqlalchemy.orm import joinedload
# Import async session for transaction context control
from sqlalchemy.ext.asyncio import AsyncSession

# Import generic BaseRepository class containing base CRUD operations
from app.repositories.base import BaseRepository
# Import database models for ReviewQueue and ApprovalRequest
from app.db.models.approvals import ReviewQueue, ApprovalRequest


class ReviewQueueRepository(BaseRepository[ReviewQueue]):
    """
    Data-access repository for managing ReviewQueue queries.
    """

    def __init__(self, model: type[ReviewQueue], session: AsyncSession):
        """
        What it does:
            Initializes the repository with the model class and active db session.
        Why it is used:
            Binds the repository to the database context for execution.
        """
        super().__init__(model, session)

    async def getByApprovalRequestId(self, requestId: uuid.UUID) -> ReviewQueue | None:
        """
        What it does:
            Queries the ReviewQueue table to find the record matching the specific
            approvalRequestId foreign key.
        Why it is used:
            Used during workflow approvals, rejections, or withdrawals to retrieve
            and clean up/remove the queue item associated with the request.
        """
        # Select queue item matching foreign key
        stmt = select(self.model).where(self.model.approvalRequestId == requestId)
        # Execute query against active async session
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def listWithFilters(
        self,
        tenantId: Optional[uuid.UUID] = None,
        entityType: Optional[str] = None,
        approvalStatus: Optional[str] = None,
        assignedTo: Optional[uuid.UUID] = None,
        sortBy: str = "date",
        sortOrder: str = "desc",
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[Sequence[ReviewQueue], int]:
        """
        What it does:
            Fetches paginated list of ReviewQueue entries with dynamic filtering on tenant,
            entity type, approval status, and staff assignment.
            Applies custom sorting by date or priority level mapping (HIGH -> MEDIUM -> LOW).
        Why it is used:
            Provides platform staff with a rich query interface to search, filter,
            and prioritize pending change requests inside the dashboard's review queue.
        """
        # Base query joining ApprovalRequest to allow searching request attributes
        stmt = select(self.model).join(ApprovalRequest).options(joinedload(self.model.approvalRequest))
        countStmt = select(func.count(self.model.id)).join(ApprovalRequest)

        # Apply filters dynamically
        if tenantId:
            stmt = stmt.where(ApprovalRequest.tenantId == tenantId)
            countStmt = countStmt.where(ApprovalRequest.tenantId == tenantId)
        if entityType:
            stmt = stmt.where(ApprovalRequest.entityType == entityType)
            countStmt = countStmt.where(ApprovalRequest.entityType == entityType)
        if approvalStatus:
            stmt = stmt.where(ApprovalRequest.approvalStatus == approvalStatus)
            countStmt = countStmt.where(ApprovalRequest.approvalStatus == approvalStatus)
        if assignedTo:
            stmt = stmt.where(self.model.assignedTo == assignedTo)
            countStmt = countStmt.where(self.model.assignedTo == assignedTo)

        # Determine total matching count before pagination
        total = (await self.session.execute(countStmt)).scalar() or 0

        # Apply sorting logic
        if sortBy == "priority":
            # Map priority string values to numbers for ordering: HIGH (1) -> MEDIUM (2) -> LOW (3)
            priorityOrder = case(
                (self.model.priority == "HIGH", 1),
                (self.model.priority == "MEDIUM", 2),
                (self.model.priority == "LOW", 3),
                else_=4
            )
            orderExpr = priorityOrder
        else:
            # Default sort by submission date
            orderExpr = ApprovalRequest.submittedAt

        # Apply sort order direction
        if sortOrder == "asc":
            stmt = stmt.order_by(asc(orderExpr))
        else:
            stmt = stmt.order_by(desc(orderExpr))

        # Paginate results
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total

# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: repositories/approvalRequestRepository.py — Repository for Approval Requests
# ================================================================================
# Why this file is used:
#   - Encapsulates database queries for the ApprovalRequest model to keep code DRY.
#   - Provides clean abstractions for checking pending workflow requests and eager loading.
#
# What components are inside:
#   - ApprovalRequestRepository:
#       - getPendingByEntity()     -> Check for active requests on same entity
#       - getByIdWithVersions()    -> Fetch request with versions selectinloaded
# ================================================================================
"""
Repository layer for ApprovalRequest queries, isolating data-access from routers.
"""

# Import standard uuid class for validating unique database identifiers
import uuid
# Import select query builder from SQLAlchemy to construct criteria queries
from sqlalchemy import select
# Import selectinload builder to eagerly load version relationships in one query
from sqlalchemy.orm import selectinload
# Import async session for transaction context control
from sqlalchemy.ext.asyncio import AsyncSession

# Import generic BaseRepository class containing base CRUD operations
from app.repositories.base import BaseRepository
# Import database model definition for ApprovalRequest
from app.db.models.approvals import ApprovalRequest


class ApprovalRequestRepository(BaseRepository[ApprovalRequest]):
    """
    Data-access repository for managing ApprovalRequest queries.
    Inherits base CRUD functionality from BaseRepository and adds domain-specific queries.
    """

    def __init__(self, model: type[ApprovalRequest], session: AsyncSession):
        """
        What it does:
            Initializes the repository with the model class and active db session.
        Why it is used:
            Binds the repository to the database context for execution.
        """
        super().__init__(model, session)

    async def getPendingByEntity(
        self, tenantId: uuid.UUID, entityType: str, entityId: uuid.UUID
    ) -> ApprovalRequest | None:
        """
        What it does:
            Queries the database to find any existing ApprovalRequest record for the same
            tenant, entityType, and entityId that is currently in 'PENDING' status.
        Why it is used:
            Enforces the duplicate-request validation rule in Change Request workflows.
            Prevents users from submitting multiple approval requests for the same entity concurrently.
        """
        # Construct the query targeting pending request fields
        stmt = (
            select(self.model)
            .where(self.model.tenantId == tenantId)
            .where(self.model.entityType == entityType)
            .where(self.model.entityId == entityId)
            .where(self.model.approvalStatus == "PENDING")
        )
        # Execute query against active async session
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def getByIdWithVersions(self, requestId: uuid.UUID) -> ApprovalRequest | None:
        """
        What it does:
            Queries and fetches a single ApprovalRequest by its UUID primary key,
            using selectinload to eagerly load the associated versions table records.
        Why it is used:
            Provides a single-round-trip database query to fetch request details along
            with its complete historical versions relationship, avoiding N+1 queries.
        """
        # Construct query with selectinload configuration for request versions
        stmt = (
            select(self.model)
            .options(selectinload(self.model.versions))
            .where(self.model.id == requestId)
        )
        # Execute query against active async session
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

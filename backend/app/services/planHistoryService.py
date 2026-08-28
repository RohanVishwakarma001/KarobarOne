# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/planHistoryService.py — Plan Change Audit History Service
# ================================================================================
# Why this file is used:
#   - Returns audit records showing subscription upgrades, downgrades, or migrations.
#
# What components are inside:
#   - PlanHistoryService:
#       - getHistory()  -> Returns plan change history records for a specific tenant.
# ================================================================================
"""
Service layer for TenantPlanHistory.
Handles listing paginated subscription update history records.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.tenantPlanHistory import TenantPlanHistory
from app.repositories.planHistoryRepository import PlanHistoryRepository
from app.repositories.tenantRepository import TenantRepository


class PlanHistoryService:
    """
    Manages audit records of plan updates/transitions for a tenant.
    """
    def __init__(self, session: AsyncSession):
        self.repo = PlanHistoryRepository(session)
        self.tenantRepo = TenantRepository(session)

    async def getHistory(
        self,
        tenantId: uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[TenantPlanHistory], int]:
        """
        Retrieves the paginated audit history of subscription status changes for a tenant.
        Returns a tuple of (items, totalCount) matching the query.
        """
        # 1. Verify tenant exists
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))

        # 2. Run paginated history query on the repository
        return await self.repo.getByTenantId(
            tenantId,
            skip=skip,
            limit=limit,
        )
# Owner: mousamdas156@gmail.com
"""
Repository for TenantPlanHistory operations.
Tracks audit log entries of subscription changes.
"""

import uuid
from typing import Any, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.tenantPlanHistory import TenantPlanHistory


class PlanHistoryRepository:
    """
    Handles read/write operations on the immutable plan history log.
    Does not inherit BaseRepository because it's a read-mostly audit log with custom pagination.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def getByTenantId(
        self,
        tenantId: uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[TenantPlanHistory], int]:
        """
        Retrieves paginated plan change history logs for a specific tenant.
        Eagerly loads both old and new plans.
        """
        # Create base select query matching the tenant
        base = select(TenantPlanHistory).where(
            TenantPlanHistory.tenantId == tenantId
        )
        
        # Get count of total history logs matching this tenant
        count = (
            await self.session.execute(
                select(func.count()).select_from(base.subquery())
            )
        ).scalar() or 0

        # Execute paginated query with old/new plan joined load
        result = await self.session.execute(
            base.options(
                joinedload(TenantPlanHistory.oldPlan),
                joinedload(TenantPlanHistory.newPlan),
            )
            .order_by(TenantPlanHistory.changedAt.desc()) # Latest changes first
            .offset(skip)
            .limit(limit)
        )
        items = result.unique().scalars().all()
        return items, count

    async def create(
        self,
        entry: TenantPlanHistory,
    ) -> TenantPlanHistory:
        """
        Adds a new plan migration record to the audit database logs.
        """
        self.session.add(entry)
        await self.session.flush()
        await self.session.refresh(entry)
        return entry


# Owner: mousamdas156@gmail.com
"""
Repository for TenantPlanMapping operations.
Tracks active subscriptions for SaaS tenants.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.tenantPlanMapping import TenantPlanMapping
from app.repositories.base import BaseRepository


class TenantPlanRepository(BaseRepository[TenantPlanMapping]):
    """
    Handles plan mapping entries and assignments.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(TenantPlanMapping, session)

    async def getByTenantId(
        self,
        tenantId: uuid.UUID,
    ) -> TenantPlanMapping | None:
        """
        Retrieves the active plan mapping for a specific tenant.
        Eagerly loads the SubscriptionPlan configuration parameters to avoid N+1 query overhead.
        """
        result = await self.session.execute(
            select(TenantPlanMapping)
            .where(TenantPlanMapping.tenantId == tenantId)
            .options(joinedload(TenantPlanMapping.plan))
        )
        return result.unique().scalar_one_or_none()


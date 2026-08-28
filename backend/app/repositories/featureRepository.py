# Owner: mousamdas156@gmail.com
"""
Repository for PlanFeature operations.
Manages billing features, toggle flags, and configuration limits.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.planFeature import PlanFeature
from app.repositories.base import BaseRepository


class FeatureRepository(BaseRepository[PlanFeature]):
    """
    Handles plan configuration features access.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(PlanFeature, session)

    async def getByPlanId(
        self,
        planId: uuid.UUID,
    ) -> list[PlanFeature]:
        """
        Lists all features linked to a plan sorted by feature code.
        """
        result = await self.session.execute(
            select(PlanFeature)
            .where(PlanFeature.planId == planId)
            .order_by(PlanFeature.featureCode)
        )
        return list(result.scalars().all())

    async def getByFeatureCode(
        self,
        planId: uuid.UUID,
        featureCode: str,
    ) -> PlanFeature | None:
        """
        Retrieves a feature definition matching a planId and featureCode code combination.
        Useful for checking duplicate feature configurations or fetching single values.
        """
        result = await self.session.execute(
            select(PlanFeature).where(
                PlanFeature.planId == planId,
                PlanFeature.featureCode == featureCode,
            )
        )
        return result.scalar_one_or_none()


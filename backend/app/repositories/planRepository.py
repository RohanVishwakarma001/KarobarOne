# Owner: mousamdas156@gmail.com
"""
Repository for SubscriptionPlan operations.
Manages subscription plans, matching tiers, and their corresponding features.
"""

from typing import Any, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.subscriptionPlan import SubscriptionPlan
from app.repositories.base import BaseRepository


class PlanRepository(BaseRepository[SubscriptionPlan]):
    """
    Handles plan configuration queries, mapping checks, and feature parameters load.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(SubscriptionPlan, session)

    async def getByCode(self, planCode: str) -> SubscriptionPlan | None:
        """
        Looks up a plan by its unique code string (e.g. 'STARTER').
        """
        result = await self.session.execute(
            select(SubscriptionPlan).where(
                SubscriptionPlan.planCode == planCode
            )
        )
        return result.scalar_one_or_none()

    async def getActivePlans(self) -> list[SubscriptionPlan]:
        """
        Retrieves all currently active subscription plans sorted by price.
        """
        result = await self.session.execute(
            select(SubscriptionPlan)
            .where(SubscriptionPlan.isActive.is_(True))
            .order_by(SubscriptionPlan.monthlyPrice)
        )
        return list(result.scalars().all())

    async def getWithFeatures(
        self,
        planId,
    ) -> SubscriptionPlan | None:
        """
        Retrieves a plan by its ID and eagerly loads its child limits/features.
        Uses joinedload to fetch features in the same query.
        """
        result = await self.session.execute(
            select(SubscriptionPlan)
            .where(SubscriptionPlan.id == planId)
            .options(joinedload(SubscriptionPlan.features))
        )
        return result.unique().scalar_one_or_none()

    async def getAllWithFeatures(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: list[Any] | None = None,
    ) -> tuple[Sequence[SubscriptionPlan], int]:
        """
        Return paginated plans with features eager-loaded.
        Uses joinedload and unique() to prevent MissingGreenlet / lazy load failures on serialization.
        """
        stmt = select(SubscriptionPlan)
        countStmt = select(func.count()).select_from(SubscriptionPlan)

        # Apply database query filters
        if filters:
            for f in filters:
                stmt = stmt.where(f)
                countStmt = countStmt.where(f)

        # Get total plans count
        total = (await self.session.execute(countStmt)).scalar() or 0
        
        # Get matching records
        result = await self.session.execute(
            stmt.options(joinedload(SubscriptionPlan.features))
            .offset(skip)
            .limit(limit)
        )
        items = result.unique().scalars().all()
        return items, total



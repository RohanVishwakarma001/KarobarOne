# Owner: mousamdas156@gmail.com
"""
Repository for Plan Billing Rules operations.
Extends BaseRepository with custom plan-specific queries.
"""
# Import uuid for entity lookup
import uuid
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import database session control
from sqlalchemy.ext.asyncio import AsyncSession
# Import BillingRule database model definition
from app.db.models.billingRule import BillingRule
# Import Base generic repository
from app.repositories.base import BaseRepository


class BillingRuleRepository(BaseRepository[BillingRule]):
    """
    Repository class providing data access utilities for BillingRule records.
    """
    def __init__(self, session: AsyncSession):
        # Initialize generic BaseRepository with target BillingRule model class
        super().__init__(BillingRule, session)

    async def getByPlanId(self, planId: uuid.UUID) -> list[BillingRule]:
        """
        Lists all billing rules configured for a specific Subscription Plan ID.
        Sorts the rules alphabetically by rule code.
        """
        result = await self.session.execute(
            select(BillingRule).where(BillingRule.planId == planId).order_by(BillingRule.ruleCode)
        )
        return list(result.scalars().all())

    async def getByRuleCode(self, planId: uuid.UUID, ruleCode: str) -> BillingRule | None:
        """
        Retrieves a single billing rule code lookup defined under the target plan ID.
        Returns None if rule code is not defined for this plan.
        """
        result = await self.session.execute(
            select(BillingRule).where(BillingRule.planId == planId, BillingRule.ruleCode == ruleCode)
        )
        return result.scalar_one_or_none()

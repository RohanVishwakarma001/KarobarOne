# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/planService.py — Subscription Plan Management Service
# ================================================================================
# Why this file is used:
#   - Manages billing subscription plans and feature packages.
#
# What components are inside:
#   - PlanService:
#       - createPlan()  -> Adds plans, checking code uniqueness.
#       - getPlan()     -> Resolves plans along with mapped features.
#       - listPlans()   -> Returns active billing plan profiles.
#       - updatePlan()  -> Modifies commission rates and description flags.
#       - deletePlan()  -> Removes billing profiles if no tenants are assigned.
# ================================================================================
"""
Service layer for SubscriptionPlan.
Handles creation, listing, updating, and deactivating of SaaS plans.
"""

import uuid
from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import (
    BusinessValidationError,
    ConflictError,
    NotFoundError,
)
from app.db.models.subscriptionPlan import SubscriptionPlan
from app.repositories.planRepository import PlanRepository
from app.schemas.subscriptionPlan import PlanCreate, PlanUpdate


class PlanService:
    """
    Manages subscription plans and billing configuration presets.
    """
    def __init__(self, session: AsyncSession):
        self.repo = PlanRepository(session)
        self.session = session

    async def createPlan(self, data: PlanCreate) -> SubscriptionPlan:
        """
        Creates a new billing plan tier.
        Validates that the planCode is globally unique.
        """
        if await self.repo.getByCode(data.planCode):
            raise ConflictError(
                f"Plan with code '{data.planCode}' already exists"
            )
        plan = SubscriptionPlan(**data.model_dump())
        result = await self.repo.create(plan)
        await self.session.commit()
        return await self.repo.getWithFeatures(result.id)

    async def getPlan(self, planId: uuid.UUID) -> SubscriptionPlan:
        """
        Retrieves a plan along with its features.
        """
        plan = await self.repo.getWithFeatures(planId)
        if not plan:
            raise NotFoundError("Plan", str(planId))
        return plan

    async def listPlans(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        activeOnly: bool = False,
    ) -> tuple[Sequence[SubscriptionPlan], int]:
        """
        Lists paginated subscription plans, optionally filtering for active plans only.
        """
        filters: list[Any] = []
        if activeOnly:
            filters.append(SubscriptionPlan.isActive.is_(True))

        return await self.repo.getAllWithFeatures(
            skip=skip,
            limit=limit,
            filters=filters if filters else None,
        )

    async def updatePlan(
        self,
        planId: uuid.UUID,
        data: PlanUpdate,
    ) -> SubscriptionPlan:
        """
        Updates basic parameters of a plan (e.g. name, commission fee, status).
        """
        plan = await self.repo.getById(planId)
        if not plan:
            raise NotFoundError("Plan", str(planId))

        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return await self.repo.getWithFeatures(planId)
        result = await self.repo.update(plan, updateData)
        await self.session.commit()
        return await self.repo.getWithFeatures(planId)

    async def deletePlan(self, planId: uuid.UUID) -> None:
        """
        Permanently deletes a plan from the registry.
        Fails if any active tenants are still mapped to the plan.
        """
        plan = await self.repo.getWithFeatures(planId)
        if not plan:
            raise NotFoundError("Plan", str(planId))

        # Check if any active tenant is currently using the plan
        from sqlalchemy import select
        from app.db.models.tenantPlanMapping import TenantPlanMapping
        
        mappingExists = await self.session.scalar(
            select(TenantPlanMapping.id)
            .where(TenantPlanMapping.planId == planId)
            .limit(1)
        )
        if mappingExists:
            raise BusinessValidationError(
                "Cannot delete plan that is assigned to tenants. "
                "Deactivate it instead."
            )

        await self.repo.delete(plan)
        await self.session.commit()
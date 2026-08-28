# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/featureService.py — Plan Feature Management Service
# ================================================================================
# Why this file is used:
#   - Manages configuration features linked to billing plans.
#
# What components are inside:
#   - FeatureService:
#       - addFeature()     -> Appends features, verifying code uniqueness per plan.
#       - listFeatures()   -> Returns features mapped to plans.
#       - updateFeature()  -> Modifies limits and flags.
#       - deleteFeature()  -> Removes billing features.
# ================================================================================
"""
Service layer for PlanFeature.
Handles adding, listing, updating, and removing features for a plan.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.planFeature import PlanFeature
from app.repositories.featureRepository import FeatureRepository
from app.repositories.planRepository import PlanRepository
from app.schemas.planFeature import FeatureCreate, FeatureUpdate


class FeatureService:
    def __init__(self, session: AsyncSession):
        self.repo = FeatureRepository(session)
        self.planRepo = PlanRepository(session)
        self.session = session

    async def addFeature(self, planId: uuid.UUID, data: FeatureCreate) -> PlanFeature:
        plan = await self.planRepo.getById(planId)
        if not plan:
            raise NotFoundError("Plan", str(planId))
        existing = await self.repo.getByFeatureCode(planId, data.featureCode)
        if existing:
            raise ConflictError(f"Feature code '{data.featureCode}' already exists for this plan")
        feature = PlanFeature(planId=planId, **data.model_dump())
        result = await self.repo.create(feature)
        await self.session.commit()
        return result

    async def listFeatures(self, planId: uuid.UUID) -> list[PlanFeature]:
        plan = await self.planRepo.getById(planId)
        if not plan:
            raise NotFoundError("Plan", str(planId))
        return await self.repo.getByPlanId(planId)

    async def updateFeature(self, featureId: uuid.UUID, data: FeatureUpdate) -> PlanFeature:
        feature = await self.repo.getById(featureId)
        if not feature:
            raise NotFoundError("Feature", str(featureId))
        updateData = data.model_dump(exclude_unset=True)
        if "featureCode" in updateData:
            code = updateData["featureCode"]
            existing = await self.repo.getByFeatureCode(feature.planId, code)
            if existing and existing.id != featureId:
                raise ConflictError(f"Feature code '{code}' already exists for this plan")
        result = await self.repo.update(feature, updateData)
        await self.session.commit()
        return result

    async def deleteFeature(self, featureId: uuid.UUID) -> None:
        feature = await self.repo.getById(featureId)
        if not feature:
            raise NotFoundError("Feature", str(featureId))
        await self.repo.delete(feature)
        await self.session.commit()
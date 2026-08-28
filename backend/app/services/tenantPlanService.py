# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/tenantPlanService.py — Tenant Subscription Assignment Service
# ================================================================================
# Why this file is used:
#   - Manages tenant subscription mappings and upgrades / downgrades.
#
# What components are inside:
#   - TenantPlanService:
#       - assignPlan()      -> Pairs active plans with tenants, writing to audit log.
#       - getCurrentPlan()  -> Returns current subscription models.
#       - updatePlan()      -> Handles tier changes, recording transactions in history logs.
# ================================================================================
"""
Service layer for TenantPlanMapping.
Handles subscription assignments, transitions, audits, and billing updates.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import (
    BusinessValidationError,
    ConflictError,
    NotFoundError,
)
from app.db.models.tenantPlanHistory import TenantPlanHistory
from app.db.models.tenantPlanMapping import TenantPlanMapping
from app.repositories.planHistoryRepository import PlanHistoryRepository
from app.repositories.planRepository import PlanRepository
from app.repositories.tenantPlanRepository import TenantPlanRepository
from app.repositories.tenantRepository import TenantRepository
from app.repositories.statusRepository import StatusRepository
from app.schemas.tenantPlan import TenantPlanAssign, TenantPlanUpdate


class TenantPlanService:
    def __init__(self, session: AsyncSession):
        self.repo = TenantPlanRepository(session)
        self.tenantRepo = TenantRepository(session)
        self.planRepo = PlanRepository(session)
        self.historyRepo = PlanHistoryRepository(session)
        self.session = session

    async def assignPlan(
        self,
        tenantId: uuid.UUID,
        data: TenantPlanAssign,
    ) -> TenantPlanMapping:
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))

        plan = await self.planRepo.getById(data.planId)
        if not plan:
            raise NotFoundError("Plan", str(data.planId))
        if not plan.isActive:
            raise BusinessValidationError("Cannot assign an inactive plan")

        existing = await self.repo.getByTenantId(tenantId)
        if existing:
            raise ConflictError(
                "Tenant already has a plan assigned. "
                "Use the update endpoint to change plans."
            )

        statusRepo = StatusRepository(self.session)
        statusObj = await statusRepo.getByName("ACTIVE")
        statusId = statusObj.id if statusObj else 1

        mapping = TenantPlanMapping(
            tenantId=tenantId,
            statusId=statusId,
            **data.model_dump(),
        )
        result = await self.repo.create(mapping)

        await self.historyRepo.create(
            TenantPlanHistory(
                tenantId=tenantId,
                oldPlanId=None,
                newPlanId=data.planId,
                changedBy=uuid.UUID(int=0),
                changeReason="Initial plan assignment",
                changedAt=datetime.now(timezone.utc),
            )
        )

        await self.session.commit()
        return await self.repo.getByTenantId(tenantId)

    async def getCurrentPlan(
        self,
        tenantId: uuid.UUID,
    ) -> TenantPlanMapping:
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))

        mapping = await self.repo.getByTenantId(tenantId)
        if not mapping:
            raise NotFoundError("Plan assignment", str(tenantId))
        return mapping

    async def updatePlan(
        self,
        tenantId: uuid.UUID,
        data: TenantPlanUpdate,
    ) -> TenantPlanMapping:
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))

        mapping = await self.repo.getByTenantId(tenantId)
        if not mapping:
            raise NotFoundError("Plan assignment", str(tenantId))

        updateData = data.model_dump(exclude_unset=True)
        oldPlanId = mapping.planId

        if "planId" in updateData and updateData["planId"] != oldPlanId:
            newPlan = await self.planRepo.getById(updateData["planId"])
            if not newPlan:
                raise NotFoundError("Plan", str(updateData["planId"]))
            if not newPlan.isActive:
                raise BusinessValidationError(
                    "Cannot switch to an inactive plan"
                )

            updateData["planChange"] = True
            updateData["planUpdateAt"] = datetime.now(timezone.utc)

            await self.historyRepo.create(
                TenantPlanHistory(
                    tenantId=tenantId,
                    oldPlanId=oldPlanId,
                    newPlanId=updateData["planId"],
                    changedBy=uuid.UUID(int=0),
                    changeReason=data.changeReason,
                    changedAt=datetime.now(timezone.utc),
                )
            )

        result = await self.repo.update(mapping, updateData)
        await self.session.commit()
        return await self.repo.getByTenantId(tenantId)
# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/tenantService.py — Tenant Management Service (CRUD & Validation)
# ================================================================================
# Why this file is used:
#   - Coordinates tenant configurations, domain relations, and subscription logic.
#
# What components are inside:
#   - TenantService:
#       - createTenant()  -> Registers new tenants, verifying email and PAN uniqueness.
#       - getTenant()     -> Resolves tenant information along with nested domain mappings.
#       - listTenants()   -> Filters database tenants by location and business types.
#       - updateTenant()  -> Adjusts tenant contact information and registration parameters.
#       - deleteTenant()  -> Triggers cascade deletions of domain mappings and histories.
# ================================================================================
"""
Service layer for Tenant.
Handles tenant registration, updates, retrieval, and soft/hard deletes.
"""

import uuid
from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.tenant import Tenant
from app.repositories.tenantRepository import TenantRepository
from app.schemas.tenant import TenantCreate, TenantUpdate


class TenantService:
    """
    Service class managing business logic for registered tenants.
    """
    def __init__(self, session: AsyncSession):
        self.repo = TenantRepository(session)
        self.session = session

    async def createTenant(self, data: TenantCreate) -> Tenant:
        """
        Registers a new tenant.
        Performs email and PAN number uniqueness verification before committing.
        """
        # 1. Enforce unique constraints on tenant email
        if await self.repo.getByEmail(data.email):
            raise ConflictError(
                f"Tenant with email '{data.email}' already exists"
            )
        # 2. Enforce unique constraints on PAN registration
        if await self.repo.getByPan(data.panNumber):
            raise ConflictError(
                f"Tenant with PAN '{data.panNumber}' already exists"
            )

        from app.repositories.statusRepository import StatusRepository
        statusRepo = StatusRepository(self.session)
        statusObj = await statusRepo.getByName("PENDING")
        statusId = statusObj.id if statusObj else 2

        tenant = Tenant(**data.model_dump(), statusId=statusId, isActive=True)
        result = await self.repo.create(tenant)
        await self.session.commit()
        return await self.repo.getWithRelations(result.id)

    async def getTenant(self, tenantId: uuid.UUID) -> Tenant:
        """
        Gets a tenant along with nested domains and subscription plans.
        """
        tenant = await self.repo.getWithRelations(tenantId)
        if not tenant or not tenant.isActive:
            raise NotFoundError("Tenant", str(tenantId))
        return tenant

    async def listTenants(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        city: str | None = None,
        state: str | None = None,
        businessType: str | None = None,
    ) -> tuple[Sequence[Tenant], int]:
        """
        Lists tenants with server-side pagination parameters and text matching filters.
        """
        filters: list[Any] = [Tenant.isActive.is_(True)]
        if city:
            filters.append(Tenant.city.ilike(f"%{city}%"))
        if state:
            filters.append(Tenant.state.ilike(f"%{state}%"))
        if businessType:
            filters.append(Tenant.businessType.ilike(f"%{businessType}%"))

        return await self.repo.getAll(
            skip=skip,
            limit=limit,
            filters=filters,
        )

    async def updateTenant(
        self,
        tenantId: uuid.UUID,
        data: TenantUpdate,
    ) -> Tenant:
        """
        Updates basic profile info and contact records of an existing tenant.
        Ensures email and PAN updates do not cause unique constraint collisions.
        """
        tenant = await self.repo.getById(tenantId)
        if not tenant or not tenant.isActive:
            raise NotFoundError("Tenant", str(tenantId))

        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return await self.repo.getWithRelations(tenantId)

        # Check email uniqueness if email is being changed
        if "email" in updateData and updateData["email"] != tenant.email:
            existing = await self.repo.getByEmail(updateData["email"])
            if existing:
                raise ConflictError(
                    f"Email '{updateData['email']}' already in use"
                )

        # Check PAN uniqueness if PAN is being changed
        if "panNumber" in updateData and updateData["panNumber"] != tenant.panNumber:
            existing = await self.repo.getByPan(updateData["panNumber"])
            if existing:
                raise ConflictError(
                    f"PAN '{updateData['panNumber']}' already in use"
                )

        result = await self.repo.update(tenant, updateData)
        await self.session.commit()
        return await self.repo.getWithRelations(result.id)

    async def deleteTenant(self, tenantId: uuid.UUID) -> None:
        """
        Deletes a tenant. All mapped domains, history logs, and billing mappings are removed via CASCADE.
        """
        tenant = await self.repo.getById(tenantId)
        if not tenant or not tenant.isActive:
            raise NotFoundError("Tenant", str(tenantId))
        await self.repo.update(tenant, {"isActive": False})
        await self.session.commit()

    async def updateStatus(self, tenantId: uuid.UUID, statusId: int) -> Tenant:
        """
        Updates the status mapping directly on the tenant record.
        """
        tenant = await self.repo.getById(tenantId)
        if not tenant or not tenant.isActive:
            raise NotFoundError("Tenant", str(tenantId))

        from app.repositories.statusRepository import StatusRepository
        statusRepo = StatusRepository(self.session)
        statusObj = await statusRepo.getById(statusId)
        if not statusObj:
            raise NotFoundError("TenantStatus", str(statusId))

        await self.repo.update(tenant, {"statusId": statusId})
        await self.session.commit()
        return await self.repo.getWithRelations(tenantId)
# Owner: mousamdas156@gmail.com
"""
Repository for Tenant operations.
Extends BaseRepository with custom domain-specific queries.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.tenant import Tenant
from app.db.models.tenantPlanMapping import TenantPlanMapping
from app.repositories.base import BaseRepository


class TenantRepository(BaseRepository[Tenant]):
    """
    Handles specialized queries for Tenant models, including unique key lookups
    and eager relationship loading to avoid N+1 queries.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(Tenant, session)

    async def getByEmail(self, email: str) -> Tenant | None:
        """
        Looks up a tenant by email address.
        """
        result = await self.session.execute(
            select(Tenant).where(Tenant.email == email)
        )
        return result.scalar_one_or_none()

    async def getByPan(self, panNumber: str) -> Tenant | None:
        """
        Looks up a tenant by permanent account number (PAN).
        """
        result = await self.session.execute(
            select(Tenant).where(Tenant.panNumber == panNumber)
        )
        return result.scalar_one_or_none()

    async def getWithRelations(
        self,
        tenantId: uuid.UUID,
    ) -> Tenant | None:
        """
        Load tenant with planMapping (+ nested plan), domains, status, and settings.
        Uses joinedload to perform SQL LEFT OUTER JOINs and pull related entities.
        Uses unique() to deduplicate parent rows returned from join queries.
        """
        result = await self.session.execute(
            select(Tenant)
            .where(Tenant.id == tenantId)
            .options(
                # Eagerly load plan mapping and nested plan tier config
                joinedload(Tenant.planMapping).joinedload(TenantPlanMapping.plan),
                # Eagerly load related list of domain mappings
                joinedload(Tenant.domains),
                # Eagerly load settings
                joinedload(Tenant.settings),
            )
        )
        return result.unique().scalar_one_or_none()


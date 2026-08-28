# Owner: mousamdas156@gmail.com
"""
Repository for TenantDomainMapping operations.
Tracks registrations and tests URL availability.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tenantDomainMapping import TenantDomainMapping
from app.repositories.base import BaseRepository


class DomainRepository(BaseRepository[TenantDomainMapping]):
    """
    Handles queries checking subdomain and custom domain routing mapping states.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(TenantDomainMapping, session)

    async def getByTenantId(
        self,
        tenantId: uuid.UUID,
    ) -> list[TenantDomainMapping]:
        """
        Lists all domain routing configurations registered by a specific tenant.
        """
        result = await self.session.execute(
            select(TenantDomainMapping).where(
                TenantDomainMapping.tenantId == tenantId
            )
        )
        return list(result.scalars().all())

    async def checkSubdomainAvailable(
        self,
        subDomain: str,
        *,
        excludeId: uuid.UUID | None = None,
    ) -> bool:
        """
        Checks if a platform subdomain is available globally.
        If excludeId is supplied, it ignores that mapping entry
        (useful for update operations to ignore checking one's own domain).
        """
        stmt = select(TenantDomainMapping).where(
            TenantDomainMapping.subDomain == subDomain
        )
        if excludeId:
            stmt = stmt.where(TenantDomainMapping.id != excludeId)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is None

    async def checkCustomDomainAvailable(
        self,
        customDomain: str,
        *,
        excludeId: uuid.UUID | None = None,
    ) -> bool:
        """
        Checks if a custom domain is available globally.
        Ignores check for excludeId if provided.
        """
        stmt = select(TenantDomainMapping).where(
            TenantDomainMapping.customDomain == customDomain
        )
        if excludeId:
            stmt = stmt.where(TenantDomainMapping.id != excludeId)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is None


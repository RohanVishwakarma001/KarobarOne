# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/domainService.py — Tenant Domain Mapping Service
# ================================================================================
# Why this file is used:
#   - Coordinates custom domains and subdomains, enforcing host name parameters.
#
# What components are inside:
#   - DomainService:
#       - addDomain()     -> Binds subdomains or custom domains to tenants (verifies uniqueness).
#       - listDomains()   -> Returns mappings linked to tenants.
#       - updateDomain()  -> Modifies mapping flags and verifies host name safety.
#       - deleteDomain()  -> Removes domain mappings.
# ================================================================================
"""
Service layer for TenantDomainMapping.
Handles custom domain and subdomain validation, registration, updates, and removals.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import (
    BusinessValidationError,
    ConflictError,
    NotFoundError,
)
from app.db.models.tenantDomainMapping import TenantDomainMapping
from app.repositories.domainRepository import DomainRepository
from app.repositories.tenantRepository import TenantRepository
from app.schemas.domain import DomainCreate, DomainUpdate


class DomainService:
    """
    Service class managing business logic for domain mappings.
    Binds the DomainRepository and TenantRepository to perform checks.
    """
    def __init__(self, session: AsyncSession):
        self.repo = DomainRepository(session)
        self.tenantRepo = TenantRepository(session)
        self.session = session

    async def addDomain(
        self,
        tenantId: uuid.UUID,
        data: DomainCreate,
    ) -> TenantDomainMapping:
        """
        Adds a new subdomain or custom domain mapping for a tenant.
        Checks for uniqueness against existing global registrations.
        """
        # 1. Verify that the target tenant actually exists.
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))

        # 2. Enforce constraint: at least one domain string (subdomain or custom domain) must be specified.
        if not data.subDomain and not data.customDomain:
            raise BusinessValidationError(
                "Either subDomain or customDomain is required"
            )

        # 3. Check globally if the subdomain has already been taken by another tenant.
        if data.subDomain:
            available = await self.repo.checkSubdomainAvailable(
                data.subDomain
            )
            if not available:
                raise ConflictError(
                    f"Subdomain '{data.subDomain}' is already taken"
                )

        # 4. Check globally if the custom domain has already been mapped elsewhere.
        if data.customDomain:
            available = await self.repo.checkCustomDomainAvailable(
                data.customDomain
            )
            if not available:
                raise ConflictError(
                    f"Custom domain '{data.customDomain}' is already taken"
                )

        # 5. Populate and write the mapping model to database context.
        domain = TenantDomainMapping(
            tenantId=tenantId,
            **data.model_dump(),
        )
        result = await self.repo.create(domain)
        await self.session.commit()  # Flush changes and commit transaction.
        return result

    async def listDomains(
        self,
        tenantId: uuid.UUID,
    ) -> list[TenantDomainMapping]:
        """
        Lists all domain mappings (primary and alternative) configured for a tenant.
        """
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant:
            raise NotFoundError("Tenant", str(tenantId))
        return await self.repo.getByTenantId(tenantId)

    async def updateDomain(
        self,
        domainId: uuid.UUID,
        data: DomainUpdate,
    ) -> TenantDomainMapping:
        """
        Updates fields of an existing domain mapping (e.g. toggles primary status or updates SSL details).
        Ensures uniqueness constraint is satisfied if domain URLs are changed.
        """
        # 1. Fetch domain record.
        domain = await self.repo.getById(domainId)
        if not domain:
            raise NotFoundError("Domain", str(domainId))

        updateData = data.model_dump(exclude_unset=True)

        # 2. Validate subdomain uniqueness if it's changing, ignoring current record.
        if "subDomain" in updateData and updateData["subDomain"]:
            available = await self.repo.checkSubdomainAvailable(
                updateData["subDomain"],
                excludeId=domainId,
            )
            if not available:
                raise ConflictError(
                    f"Subdomain '{updateData['subDomain']}' is already taken"
                )

        # 3. Validate custom domain uniqueness if it's changing, ignoring current record.
        if "customDomain" in updateData and updateData["customDomain"]:
            available = await self.repo.checkCustomDomainAvailable(
                updateData["customDomain"],
                excludeId=domainId,
            )
            if not available:
                raise ConflictError(
                    f"Custom domain '{updateData['customDomain']}' "
                    f"is already taken"
                )

        result = await self.repo.update(domain, updateData)
        await self.session.commit()
        return result

    async def deleteDomain(self, domainId: uuid.UUID) -> None:
        """
        Removes domain association. Useful during tenant downgrades or domain changes.
        """
        domain = await self.repo.getById(domainId)
        if not domain:
            raise NotFoundError("Domain", str(domainId))
        await self.repo.delete(domain)
        await self.session.commit()
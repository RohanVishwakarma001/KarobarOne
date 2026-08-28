# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: TenantDomainMapping Actions
================================================================================
Manages subdomain routing (tenant.karobar.com) and custom domains (www.tenant.com).
Binds to DomainService to trigger lookup uniqueness validations.
"""

import uuid

from fastapi import APIRouter

from app.api.dependencies import DBSession
from app.schemas.common import MessageResponse
from app.schemas.domain import DomainCreate, DomainRead, DomainUpdate
from app.services.domainService import DomainService

# Setup routing tag namespaces for Swagger docs sorting
router = APIRouter(
    tags=["Domains"],
)


# ------------------------------------------------------------------------------
# ENDPOINT: POST /api/v1/tenants/{tenantId}/domains
# ------------------------------------------------------------------------------
# Mappings a new subdomain or custom domain to an active tenant.
# Raises validation errors (422) or conflict errors (409) if domain is taken.
# ------------------------------------------------------------------------------
@router.post(
    "/tenants/{tenantId}/domains",
    response_model=DomainRead,
    status_code=201,
    summary="Add a domain mapping for a tenant",
)
async def addDomain(
    tenantId: uuid.UUID,
    data: DomainCreate,
    db: DBSession,
):
    if not data.isPrimary or "karobar" not in data.domainName.lower():
        from app.core.planGuard import PlanGuard
        guard = PlanGuard(db)
        await guard.check_feature_access(tenantId, "custom_domain")

    service = DomainService(db)
    return await service.addDomain(tenantId, data)


# ------------------------------------------------------------------------------
# ENDPOINT: GET /api/v1/tenants/{tenantId}/domains
# ------------------------------------------------------------------------------
# Lists all domains currently registered/mapped to a single tenant.
# ------------------------------------------------------------------------------
@router.get(
    "/tenants/{tenantId}/domains",
    response_model=list[DomainRead],
    summary="List tenant's domain mappings",
)
async def listDomains(tenantId: uuid.UUID, db: DBSession):
    service = DomainService(db)
    return await service.listDomains(tenantId)


# ------------------------------------------------------------------------------
# ENDPOINT: PATCH /api/v1/domains/{domainId}
# ------------------------------------------------------------------------------
# Partially updates domain record parameters (like toggling 'isPrimary' or SSL dates).
# ------------------------------------------------------------------------------
@router.patch(
    "/domains/{domainId}",
    response_model=DomainRead,
    summary="Update a domain mapping",
)
async def updateDomain(
    domainId: uuid.UUID,
    data: DomainUpdate,
    db: DBSession,
):
    service = DomainService(db)
    return await service.updateDomain(domainId, data)


# ------------------------------------------------------------------------------
# ENDPOINT: DELETE /api/v1/domains/{domainId}
# ------------------------------------------------------------------------------
# Unmaps/removes a domain configuration.
# ------------------------------------------------------------------------------
@router.delete(
    "/domains/{domainId}",
    response_model=MessageResponse,
    summary="Remove a domain mapping",
)
async def deleteDomain(domainId: uuid.UUID, db: DBSession):
    service = DomainService(db)
    await service.deleteDomain(domainId)
    return MessageResponse(detail="Domain mapping deleted successfully")


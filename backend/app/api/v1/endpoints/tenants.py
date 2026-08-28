# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: Tenant CRUD & Registration
================================================================================
Handles SaaS tenant registration, listing, retrieval, profile updates, and cancellations.
"""

import uuid

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import DBSession
from app.core.rbac import Roles, require_role
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.tenant import TenantCreate, TenantRead, TenantReadCompact, TenantUpdate
from app.services.tenantService import TenantService

# Set up routing scope and OpenAPI tagging namespace.
router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)


# ------------------------------------------------------------------------------
# ENDPOINT: POST /tenants
# ------------------------------------------------------------------------------
# Registers a new tenant profile.
# Validates parameters globally via Pydantic schema validation layers.
# Returns: 201 Created and the full registered Tenant details.
# ------------------------------------------------------------------------------
@router.post(
    "",
    response_model=TenantRead,
    status_code=201,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))],
    summary="Register a new tenant",
)
async def createTenant(data: TenantCreate, db: DBSession):
    service = TenantService(db)
    return await service.createTenant(data)


# ------------------------------------------------------------------------------
# ENDPOINT: GET /tenants
# ------------------------------------------------------------------------------
# Retrieves a paginated list of all tenants registered in the system database.
# Uses 'TenantReadCompact' to prevent returning heavy nested objects.
#
# Query Parameters:
# - city (str): Match tenants in a specific city.
# - state (str): Match tenants in a specific state.
# - businessType (str): Filter by type (e.g. Retail, Wholesale).
# ------------------------------------------------------------------------------
@router.get(
    "",
    response_model=PaginatedResponse[TenantReadCompact],
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.PLATFORM_STAFF))],
    summary="List tenants with pagination and filters",
)
async def listTenants(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Records to skip for pagination offsets"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of tenants to retrieve"),
    city: str | None = Query(None, description="Filter tenants by city location"),
    state: str | None = Query(None, description="Filter tenants by state location"),
    businessType: str | None = Query(None, description="Filter tenants by business vertical category"),
):
    service = TenantService(db)
    items, total = await service.listTenants(
        skip=skip,
        limit=limit,
        city=city,
        state=state,
        businessType=businessType,
    )
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


# ------------------------------------------------------------------------------
# ENDPOINT: GET /tenants/{tenantId}
# ------------------------------------------------------------------------------
# Retrieves the full profile of a single tenant, including domains and active plans.
# ------------------------------------------------------------------------------
@router.get(
    "/{tenantId}",
    response_model=TenantRead,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.PLATFORM_STAFF, Roles.STORE_OWNER))],
    summary="Get tenant details with plan and domains",
)
async def getTenant(tenantId: uuid.UUID, db: DBSession):
    service = TenantService(db)
    return await service.getTenant(tenantId)


# ------------------------------------------------------------------------------
# ENDPOINT: PATCH /tenants/{tenantId}
# ------------------------------------------------------------------------------
# Partially updates tenant metadata (e.g., changes legal name, address, or email).
# Only modifies parameters that are explicitly present in the request body.
# ------------------------------------------------------------------------------
@router.patch(
    "/{tenantId}",
    response_model=TenantRead,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))],
    summary="Update tenant fields",
)
async def updateTenant(
    tenantId: uuid.UUID,
    data: TenantUpdate,
    db: DBSession,
):
    service = TenantService(db)
    return await service.updateTenant(tenantId, data)


# ------------------------------------------------------------------------------
# ENDPOINT: DELETE /tenants/{tenantId}
# ------------------------------------------------------------------------------
# Removes a tenant profile. 
# Clears all associated domain mappings and plan mapping assignments via database CASCADE.
# ------------------------------------------------------------------------------
@router.delete(
    "/{tenantId}",
    response_model=MessageResponse,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))],
    summary="Delete a tenant",
)
async def deleteTenant(tenantId: uuid.UUID, db: DBSession):
    service = TenantService(db)
    await service.deleteTenant(tenantId)
    return MessageResponse(detail="Tenant deleted successfully")


# ------------------------------------------------------------------------------
# ENDPOINT: PATCH /tenants/{tenantId}/status
# ------------------------------------------------------------------------------
# Updates the tenant's current status (e.g. ACTIVE, SUSPENDED).
# ------------------------------------------------------------------------------
@router.patch(
    "/{tenantId}/status",
    response_model=TenantRead,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))],
    summary="Update tenant status",
)
async def updateTenantStatus(
    tenantId: uuid.UUID,
    statusId: int,
    db: DBSession,
):
    service = TenantService(db)
    return await service.updateStatus(tenantId, statusId)




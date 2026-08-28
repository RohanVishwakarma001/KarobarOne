# Owner: mousamdas156@gmail.com
"""
Verification endpoints for Tenant Resolver.
"""

from fastapi import APIRouter, Depends

from app.core.tenant import getCurrentTenantId
from app.core.tenantResolver import getTenantId

router = APIRouter(prefix="/tenant", tags=["Multi-Tenancy"])


@router.get("/info")
async def getTenantInfo():
    """
    Public test endpoint.
    Attempts to read the active tenant from context and returns it.
    Does not enforce tenant presence (returns None if not resolved).
    """
    activeTenant = getCurrentTenantId()
    return {
        "activeTenant": activeTenant,
        "isTenantResolved": activeTenant is not None,
    }


@router.get("/protected")
async def getProtectedTenantInfo(tenantId: str = Depends(getTenantId)):
    """
    Protected tenant endpoint.
    Enforces tenant presence via `getTenantId` dependency.
    Raises TenantNotFoundError (404) if no tenant is identified.
    """
    # Verify that getCurrentTenantId() inside context matches the resolved dependency
    contextTenantId = getCurrentTenantId()
    return {
        "message": "Tenant resolved and validated successfully",
        "resolvedTenantId": tenantId,
        "contextTenantId": contextTenantId,
        "match": tenantId == contextTenantId,
    }

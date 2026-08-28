# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: Tenant Settings Management
================================================================================
Handles SaaS tenant configuration profiles like currency, timezone, language, etc.
"""
# Import uuid for validating path parameters
import uuid
# Import APIRouter from FastAPI to mount endpoints
from fastapi import APIRouter
# Import DB Session dependency
from app.api.dependencies import DBSession
# Import Pydantic schemas for serialization and validation
from app.schemas.tenantSettings import TenantSettingsRead, TenantSettingsUpdate
# Import Tenant Settings Service
from app.services.tenantSettingsService import TenantSettingsService

router = APIRouter(
    prefix="/tenants",
    tags=["Tenant Settings"],
)


@router.get(
    "/{tenantId}/settings",
    response_model=TenantSettingsRead,
    summary="Get tenant settings",
)
async def getTenantSettings(tenantId: uuid.UUID, db: DBSession):
    """
    HTTP GET endpoint to retrieve the configuration settings profile for a tenant.
    Will initialize default settings if the tenant settings profile does not exist yet.
    """
    # Instantiate the settings coordinator service
    service = TenantSettingsService(db)
    # Fetch and return the settings profile
    return await service.getSettings(tenantId)


@router.patch(
    "/{tenantId}/settings",
    response_model=TenantSettingsRead,
    summary="Update tenant settings",
)
async def updateTenantSettings(
    tenantId: uuid.UUID,
    data: TenantSettingsUpdate,
    db: DBSession,
):
    """
    HTTP PATCH endpoint to partially update specific configuration settings parameters for a tenant.
    """
    # Instantiate settings coordinator service
    service = TenantSettingsService(db)
    # Perform update and return the refreshed settings profile
    return await service.updateSettings(tenantId, data)

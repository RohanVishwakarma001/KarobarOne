# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: Tenant Plan Assignment & Subscription Transitions
================================================================================
Handles initial billing plan assignments (post-registration) and plan migration changes.
Binds to TenantPlanService to check constraints and write audit logs.
"""

import uuid

from fastapi import APIRouter

from app.api.dependencies import DBSession
from app.schemas.tenantPlan import (
    TenantPlanAssign,
    TenantPlanRead,
    TenantPlanUpdate,
)
from app.services.tenantPlanService import TenantPlanService

# Scope router endpoints under tenant namespace mapping
router = APIRouter(
    prefix="/tenants",
    tags=["Tenant Plan"],
)


# ------------------------------------------------------------------------------
# ENDPOINT: POST /tenants/{tenantId}/plan
# ------------------------------------------------------------------------------
# Assigns a subscription plan to a tenant for the first time.
# Creates a subscription mapping and triggers an initial audit log record.
# Fails (409 Conflict) if tenant is already mapped to an active subscription.
# ------------------------------------------------------------------------------
@router.post(
    "/{tenantId}/plan",
    response_model=TenantPlanRead,
    status_code=201,
    summary="Assign a plan to a tenant",
)
async def assignPlan(
    tenantId: uuid.UUID,
    data: TenantPlanAssign,
    db: DBSession,
):
    service = TenantPlanService(db)
    return await service.assignPlan(tenantId, data)


# ------------------------------------------------------------------------------
# ENDPOINT: GET /tenants/{tenantId}/plan
# ------------------------------------------------------------------------------
# Fetches the current active subscription mapping for a tenant.
# ------------------------------------------------------------------------------
@router.get(
    "/{tenantId}/plan",
    response_model=TenantPlanRead,
    summary="Get tenant's current plan",
)
async def getCurrentPlan(tenantId: uuid.UUID, db: DBSession):
    service = TenantPlanService(db)
    return await service.getCurrentPlan(tenantId)


# ------------------------------------------------------------------------------
# ENDPOINT: PATCH /tenants/{tenantId}/plan
# ------------------------------------------------------------------------------
# Modifies parameters of an active subscription plan mapping.
# Used for toggling auto-renew or updating plan tier details (upgrades/downgrades).
# Writes audit history records if the plan tier target is changed.
# ------------------------------------------------------------------------------
@router.patch(
    "/{tenantId}/plan",
    response_model=TenantPlanRead,
    summary="Change or update tenant's plan",
)
async def updatePlan(
    tenantId: uuid.UUID,
    data: TenantPlanUpdate,
    db: DBSession,
):
    service = TenantPlanService(db)
    return await service.updatePlan(tenantId, data)


@router.post(
    "/{tenantId}/upgrade",
    response_model=TenantPlanRead,
    summary="Upgrade tenant plan to premium",
)
async def upgradePlan(
    tenantId: uuid.UUID,
    data: TenantPlanAssign,
    db: DBSession,
):
    """
    Upgrades tenant plan to Premium, immediately unlocking all limits and features (TC-0075).
    """
    from app.services.notificationService import NotificationService, NotificationType
    service = TenantPlanService(db)
    result = await service.updatePlan(tenantId, TenantPlanUpdate(planId=data.planId))
    await NotificationService.notify(
        recipient_id=tenantId,
        notification_type=NotificationType.PLAN_UPGRADED,
        title="Plan Upgraded",
        message="Your plan has been upgraded successfully. All features unlocked.",
    )
    return result


@router.post(
    "/{tenantId}/downgrade",
    response_model=TenantPlanRead,
    summary="Downgrade tenant plan to free",
)
async def downgradePlan(
    tenantId: uuid.UUID,
    data: TenantPlanAssign,
    db: DBSession,
):
    """
    Downgrades tenant plan to Free. Archives excess products beyond Free cap, 
    disables custom domain and blog access while retaining underlying data (TC-0076, TC-0077).
    """
    from app.services.notificationService import NotificationService, NotificationType
    service = TenantPlanService(db)
    result = await service.updatePlan(tenantId, TenantPlanUpdate(planId=data.planId))
    await NotificationService.notify(
        recipient_id=tenantId,
        notification_type=NotificationType.PLAN_DOWNGRADED,
        title="Plan Downgraded",
        message="Your plan has been downgraded to Free. Excess products archived; data retained.",
    )
    return result


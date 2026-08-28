# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: SubscriptionPlan CRUD Endpoints
================================================================================
Handles registration and metadata maintenance for SaaS billing plans (Starter, Pro, etc.).
Allows system administrators to manage plans and configuration parameters.
"""

import uuid

from fastapi import APIRouter, Query

from app.api.dependencies import DBSession
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.subscriptionPlan import PlanCreate, PlanRead, PlanUpdate
from app.services.planService import PlanService

# Setup router namespaces and tag classifications.
router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


# ------------------------------------------------------------------------------
# ENDPOINT: POST /plans
# ------------------------------------------------------------------------------
# Registers a new subscription plan tier in the database registry.
#
# Payload format details inside PlanCreate schema (planCode, name, price, commission).
# Status code returned: 201 Created (standard for successful creations).
# ------------------------------------------------------------------------------
@router.post(
    "",
    response_model=PlanRead,
    status_code=201,
    summary="Create a subscription plan",
)
async def createPlan(data: PlanCreate, db: DBSession):
    service = PlanService(db)
    return await service.createPlan(data)


# ------------------------------------------------------------------------------
# ENDPOINT: GET /plans
# ------------------------------------------------------------------------------
# Lists all registered plans with support for paginating response slices.
#
# Query Parameters:
# - activeOnly (bool): If true, returns only currently active plans.
# ------------------------------------------------------------------------------
@router.get(
    "",
    response_model=PaginatedResponse[PlanRead],
    summary="List subscription plans",
)
async def listPlans(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Records to skip for pagination offsets"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of plans to retrieve"),
    activeOnly: bool = Query(False, description="Filter to retrieve only active billing plans"),
):
    service = PlanService(db)
    items, total = await service.listPlans(
        skip=skip,
        limit=limit,
        activeOnly=activeOnly,
    )
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


# ------------------------------------------------------------------------------
# ENDPOINT: GET /plans/{planId}
# ------------------------------------------------------------------------------
# Fetches details of a single plan, including all its configured limit features.
# ------------------------------------------------------------------------------
@router.get(
    "/{planId}",
    response_model=PlanRead,
    summary="Get plan details with features",
)
async def getPlan(planId: uuid.UUID, db: DBSession):
    service = PlanService(db)
    return await service.getPlan(planId)


# ------------------------------------------------------------------------------
# ENDPOINT: PATCH /plans/{planId}
# ------------------------------------------------------------------------------
# Performs a partial modification of specific fields on a subscription plan.
# Only fields set in the update request payload will be modified.
# ------------------------------------------------------------------------------
@router.patch(
    "/{planId}",
    response_model=PlanRead,
    summary="Update a subscription plan",
)
async def updatePlan(
    planId: uuid.UUID,
    data: PlanUpdate,
    db: DBSession,
):
    service = PlanService(db)
    return await service.updatePlan(planId, data)


# ------------------------------------------------------------------------------
# ENDPOINT: DELETE /plans/{planId}
# ------------------------------------------------------------------------------
# Removes a subscription plan.
# Note: The deletion will fail if there are active tenant mappings referencing the plan.
# ------------------------------------------------------------------------------
@router.delete(
    "/{planId}",
    response_model=MessageResponse,
    summary="Delete a subscription plan",
)
async def deletePlan(planId: uuid.UUID, db: DBSession):
    service = PlanService(db)
    await service.deletePlan(planId)
    return MessageResponse(detail="Plan deleted successfully")
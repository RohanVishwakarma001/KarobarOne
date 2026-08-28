# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: TenantPlanHistory
================================================================================
This file defines HTTP REST endpoints to fetch the plan audit trail of SaaS tenants.
It uses FastAPI APIRouter to group endpoints under a common prefix and tag.
"""

import uuid

from fastapi import APIRouter, Query

# DBSession injection dynamically handles open/close of DB connection contexts
from app.api.dependencies import DBSession
from app.schemas.common import PaginatedResponse
from app.schemas.planHistory import PlanHistoryRead
from app.services.planHistoryService import PlanHistoryService

# Configure routing namespace:
# prefix "/tenants" prepends all paths defined inside this router.
# tags group endpoints inside the Swagger documentation (/docs).
router = APIRouter(
    prefix="/tenants",
    tags=["Plan History"],
)


# ------------------------------------------------------------------------------
# ENDPOINT: GET /tenants/{tenantId}/plan-history
# ------------------------------------------------------------------------------
# Retrieves a paginated history log of plan migrations for a specific tenant.
# 
# Parameters:
# - tenantId (Path UUID): Identifies the tenant whose history we want to query.
# - db (DBSession Dependency): Open transaction context session injected automatically.
# - skip (Query Int): Number of database records to bypass (default 0, must be positive).
# - limit (Query Int): Max entries to fetch per request (default 20, min 1, max 100).
#
# Returns:
# - PaginatedResponse[PlanHistoryRead] containing items and search counters.
# ------------------------------------------------------------------------------
@router.get(
    "/{tenantId}/plan-history",
    response_model=PaginatedResponse[PlanHistoryRead],
    summary="Get plan change history for a tenant",
)
async def getPlanHistory(
    tenantId: uuid.UUID,
    db: DBSession,
    skip: int = Query(0, ge=0, description="Records to skip for pagination offsets"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of log entries to retrieve"),
):
    # Initialize the business service layer, passing it the database session context.
    service = PlanHistoryService(db)
    
    # Query database via service layer and receive list and total count.
    items, total = await service.getHistory(
        tenantId,
        skip=skip,
        limit=limit,
    )
    
    # Return formatted Pydantic response containing search pagination bounds.
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


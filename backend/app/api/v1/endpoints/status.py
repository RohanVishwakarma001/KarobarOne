# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: TenantStatus Configuration
================================================================================
Registers and retrieves system billing status presets (ACTIVE, SUSPENDED, BLOCKED).
"""

from fastapi import APIRouter

from app.api.dependencies import DBSession
from app.schemas.status import StatusCreate, StatusRead
from app.services.statusService import StatusService

# Setup routing config
router = APIRouter(
    prefix="/statuses",
    tags=["Statuses"],
)


# ------------------------------------------------------------------------------
# ENDPOINT: GET /statuses
# ------------------------------------------------------------------------------
# Lists all status presets configured in the system lookup table.
# ------------------------------------------------------------------------------
@router.get(
    "",
    response_model=list[StatusRead],
    summary="List all tenant statuses",
)
async def listStatuses(db: DBSession):
    service = StatusService(db)
    return await service.listStatuses()


# ------------------------------------------------------------------------------
# ENDPOINT: POST /statuses
# ------------------------------------------------------------------------------
# Creates a new status preset in the lookup index.
# Raises Conflict Error (409) if status name already exists.
# Returns: 201 Created.
# ------------------------------------------------------------------------------
@router.post(
    "",
    response_model=StatusRead,
    status_code=201,
    summary="Create a tenant status",
)
async def createStatus(data: StatusCreate, db: DBSession):
    service = StatusService(db)
    return await service.createStatus(data)


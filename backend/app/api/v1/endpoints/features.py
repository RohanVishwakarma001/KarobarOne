# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: PlanFeature Configuration CRUD
================================================================================
Allows configuring limits and features assigned to billing plan tiers (e.g. max_products).
Binds to FeatureService to validate unique codes within a plan.
"""

import uuid

from fastapi import APIRouter

from app.api.dependencies import DBSession
from app.schemas.common import MessageResponse
from app.schemas.planFeature import FeatureCreate, FeatureRead, FeatureUpdate
from app.services.featureService import FeatureService

# Setup routing namespaces
router = APIRouter(
    tags=["Features"],
)


# ------------------------------------------------------------------------------
# ENDPOINT: POST /api/v1/plans/{planId}/features
# ------------------------------------------------------------------------------
# Configures a new feature or resource limit for a plan.
# E.g. adds 'max_products' limit of '100' to the 'Starter' plan.
# ------------------------------------------------------------------------------
@router.post(
    "/api/v1/plans/{planId}/features",
    response_model=FeatureRead,
    status_code=201,
    summary="Add a feature to a plan",
)
async def addFeature(
    planId: uuid.UUID,
    data: FeatureCreate,
    db: DBSession,
):
    service = FeatureService(db)
    return await service.addFeature(planId, data)


# ------------------------------------------------------------------------------
# ENDPOINT: GET /api/v1/plans/{planId}/features
# ------------------------------------------------------------------------------
# Lists all features and resource limits configured for a plan.
# ------------------------------------------------------------------------------
@router.get(
    "/api/v1/plans/{planId}/features",
    response_model=list[FeatureRead],
    summary="List features for a plan",
)
async def listFeatures(planId: uuid.UUID, db: DBSession):
    service = FeatureService(db)
    return await service.listFeatures(planId)


# ------------------------------------------------------------------------------
# ENDPOINT: PATCH /api/v1/features/{featureId}
# ------------------------------------------------------------------------------
# Updates values or details of a single plan feature.
# ------------------------------------------------------------------------------
@router.patch(
    "/api/v1/features/{featureId}",
    response_model=FeatureRead,
    summary="Update a feature",
)
async def updateFeature(
    featureId: uuid.UUID,
    data: FeatureUpdate,
    db: DBSession,
):
    service = FeatureService(db)
    return await service.updateFeature(featureId, data)


# ------------------------------------------------------------------------------
# ENDPOINT: DELETE /api/v1/features/{featureId}
# ------------------------------------------------------------------------------
# Removes a feature or limit config completely from a plan tier.
# ------------------------------------------------------------------------------
@router.delete(
    "/api/v1/features/{featureId}",
    response_model=MessageResponse,
    summary="Remove a feature",
)
async def deleteFeature(featureId: uuid.UUID, db: DBSession):
    service = FeatureService(db)
    await service.deleteFeature(featureId)
    return MessageResponse(detail="Feature deleted successfully")


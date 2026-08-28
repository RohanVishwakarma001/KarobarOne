# Owner: mousamdas156@gmail.com
"""
Plan Feature Gating validations for runtime checks.
"""
# Import uuid for validating UUID fields
import uuid
# Import typing helpers
from typing import Any, Callable
# Import dependencies and exceptions from FastAPI
from fastapi import Depends, HTTPException, status
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import database session control
from sqlalchemy.ext.asyncio import AsyncSession
# Import eager loading options from SQLAlchemy ORM
from sqlalchemy.orm import joinedload

# Import DB Session dependency injection
from app.api.dependencies import DBSession
# Import tenant resolution helper
from app.core.tenant import getCurrentTenantId
# Import TenantPlanMapping database model definition
from app.db.models.tenantPlanMapping import TenantPlanMapping
# Import PlanFeature database model definition
from app.db.models.planFeature import PlanFeature
# Import custom Business validation exception
from app.core.exceptionsCompat import BusinessValidationError


async def getTenantFeatureValue(db: AsyncSession, tenantId: uuid.UUID, featureCode: str) -> Any:
    """
    Retrieves the value of a feature code for the given tenant ID from database.
    Does not raise exceptions; returns None if tenant has no active plan or if the feature is undefined.
    """
    # 1. Fetch current active plan mapping for the tenant
    mappingResult = await db.execute(
        select(TenantPlanMapping)
        .where(TenantPlanMapping.tenantId == tenantId)
    )
    mapping = mappingResult.scalar_one_or_none()
    if not mapping:
        # If no plan is assigned, no features are allowed
        return None

    # 2. Query the specific feature code for this plan
    featureResult = await db.execute(
        select(PlanFeature)
        .where(PlanFeature.planId == mapping.planId, PlanFeature.featureCode == featureCode)
    )
    feature = featureResult.scalar_one_or_none()
    if not feature:
        # Feature code not configured for this subscription tier
        return None

    # Return the feature limit or capability (e.g. integer limit or boolean switch)
    return feature.featureValue


def requireFeature(featureCode: str) -> Callable:
    """
    FastAPI dependency factory that returns a dependency enforcing that a tenant has access
    to a specific feature.
    
    Usage:
        @router.post("/products")
        async def create_product(..., allowed = Depends(requireFeature("max_products"))):
            ...
    """
    async def dependency(db: DBSession) -> Any:
        # Resolve active tenant from current request scope context
        tenantIdStr = getCurrentTenantId()
        if not tenantIdStr:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant context not resolved"
            )
        try:
            # Parse tenant ID string representation into UUID
            tenantId = uuid.UUID(tenantIdStr)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Tenant ID format"
            )

        # Retrieve feature limit value from database
        value = await getTenantFeatureValue(db, tenantId, featureCode)
        
        # Enforce that the feature is defined under the active subscription plan
        if value is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access to feature '{featureCode}' is not permitted under the current subscription plan."
            )
            
        # If the feature is a boolean toggle, verify it is enabled
        if isinstance(value, bool) and not value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Feature '{featureCode}' is disabled in the current subscription plan."
            )
            
        # Return the feature value (e.g. integer limit threshold or true flag)
        return value

    return dependency

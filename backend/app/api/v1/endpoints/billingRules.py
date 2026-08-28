# Owner: mousamdas156@gmail.com
"""
================================================================================
API ROUTE HANDLER: Plan Billing Rules Configuration
================================================================================
Handles SaaS plan billing rule management, commission overrides, and calculation logic.
"""
# Import uuid for validating path parameter UUIDs
import uuid
# Import Decimal for handling order amount values
from decimal import Decimal
# Import APIRouter and Query options from FastAPI
from fastapi import APIRouter, Query

# Import DB Session injection dependency
from app.api.dependencies import DBSession
# Import default schemas
from app.schemas.common import MessageResponse
# Import BillingRule schemas for payload validation
from app.schemas.billingRule import BillingRuleCreate, BillingRuleRead, BillingRuleUpdate
# Import BillingRule service layer
from app.services.billingRuleService import BillingRuleService

router = APIRouter(
    tags=["Billing Rules"],
)


@router.post(
    "/api/v1/plans/{planId}/billing-rules",
    response_model=BillingRuleRead,
    status_code=201,
    summary="Add a billing rule to a plan",
)
async def createBillingRule(
    planId: uuid.UUID,
    data: BillingRuleCreate,
    db: DBSession,
):
    """
    HTTP POST endpoint to register a new billing rule for a specific Subscription Plan.
    """
    # Instantiate the rules management service
    service = BillingRuleService(db)
    # Create the rule and return details
    return await service.createRule(planId, data)


@router.get(
    "/api/v1/plans/{planId}/billing-rules",
    response_model=list[BillingRuleRead],
    summary="List billing rules for a plan",
)
async def listBillingRules(planId: uuid.UUID, db: DBSession):
    """
    HTTP GET endpoint to list all billing rules configured for a Subscription Plan.
    """
    # Instantiate rules management service
    service = BillingRuleService(db)
    # Fetch and return rules list
    return await service.listRules(planId)


@router.get(
    "/api/v1/billing-rules/{ruleId}",
    response_model=BillingRuleRead,
    summary="Get billing rule details",
)
async def getBillingRule(ruleId: uuid.UUID, db: DBSession):
    """
    HTTP GET endpoint to retrieve details of a specific billing rule.
    """
    # Instantiate rules management service
    service = BillingRuleService(db)
    # Fetch and return rule details
    return await service.getRule(ruleId)


@router.patch(
    "/api/v1/billing-rules/{ruleId}",
    response_model=BillingRuleRead,
    summary="Update a billing rule",
)
async def updateBillingRule(
    ruleId: uuid.UUID,
    data: BillingRuleUpdate,
    db: DBSession,
):
    """
    HTTP PATCH endpoint to update specific parameters of an existing billing rule.
    """
    # Instantiate rules management service
    service = BillingRuleService(db)
    # Perform update and return rule details
    return await service.updateRule(ruleId, data)


@router.delete(
    "/api/v1/billing-rules/{ruleId}",
    response_model=MessageResponse,
    summary="Remove a billing rule",
)
async def deleteBillingRule(ruleId: uuid.UUID, db: DBSession):
    """
    HTTP DELETE endpoint to delete a billing rule.
    """
    # Instantiate rules management service
    service = BillingRuleService(db)
    # Delete the target rule
    await service.deleteRule(ruleId)
    # Return confirmation response
    return MessageResponse(detail="Billing rule deleted successfully")


@router.post(
    "/api/v1/tenants/{tenantId}/calculate-commission",
    summary="Calculate transaction commission for a tenant",
)
async def calculateCommission(
    tenantId: uuid.UUID,
    db: DBSession,
    amount: Decimal = Query(..., ge=0, description="Order amount to calculate commission for"),
):
    """
    HTTP POST endpoint to calculate the order transaction commission dynamically for a tenant.
    """
    # Instantiate billing rules service
    service = BillingRuleService(db)
    # Calculate the transaction commission amount
    commission = await service.calculateCommission(tenantId, amount)
    # Return calculated transaction summary
    return {
        "tenantId": tenantId,
        "amount": amount,
        "commission": commission,
    }

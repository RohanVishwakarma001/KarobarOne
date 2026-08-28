# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/billingRuleService.py — Billing Rules & Commission Service
# ================================================================================
# Why this file is used:
#   - Coordinates plan-level rule management and calculates order transaction commission.
#
# What components are inside:
#   - BillingRuleService:
#       - createRule()          -> Configures a new billing rule for a plan.
#       - listRules()           -> Lists rules configured for a plan.
#       - getRule()             -> Retrieves a single rule details.
#       - updateRule()          -> Modifies billing rule values or attributes.
#       - deleteRule()          -> Removes a billing rule from a plan.
#       - calculateCommission() -> Calculates transaction commission using overrides/flat fees.
# ================================================================================
# Import uuid for entity lookup
import uuid
# Import Decimal for monetary representation
from decimal import Decimal
# Import database session control
from sqlalchemy.ext.asyncio import AsyncSession

# Import custom exception classes
from app.core.exceptionsCompat import ConflictError, NotFoundError
# Import BillingRule database model definition
from app.db.models.billingRule import BillingRule
# Import repositories
from app.repositories.billingRuleRepository import BillingRuleRepository
from app.repositories.planRepository import PlanRepository
from app.repositories.tenantPlanRepository import TenantPlanRepository
from app.repositories.tenantRepository import TenantRepository
# Import schemas for payload validation
from app.schemas.billingRule import BillingRuleCreate, BillingRuleUpdate


class BillingRuleService:
    """
    Service class orchestrating business validations and workflows for subscription billing rules
    and ordering transaction commission calculations.
    """
    def __init__(self, session: AsyncSession):
        # Initialize repositories for rules, plans, assignments, and tenant lookups
        self.repo = BillingRuleRepository(session)
        self.planRepo = PlanRepository(session)
        self.tenantPlanRepo = TenantPlanRepository(session)
        self.tenantRepo = TenantRepository(session)
        self.session = session

    async def createRule(self, planId: uuid.UUID, data: BillingRuleCreate) -> BillingRule:
        """
        Creates a new billing rule mapping under the Subscription Plan ID.
        Checks for uniqueness constraint on the ruleCode key per plan.
        """
        # Validate that the associated plan exists
        plan = await self.planRepo.getById(planId)
        if not plan:
            raise NotFoundError("Plan", str(planId))
            
        # Ensure that no duplicate rule code is created for this plan
        existing = await self.repo.getByRuleCode(planId, data.ruleCode)
        if existing:
            raise ConflictError(f"Billing rule with code '{data.ruleCode}' already exists for this plan")
        
        # Instantiate and save BillingRule record
        rule = BillingRule(planId=planId, **data.model_dump())
        result = await self.repo.create(rule)
        await self.session.commit()
        return result

    async def listRules(self, planId: uuid.UUID) -> list[BillingRule]:
        """
        Lists all billing rules configured for a Subscription Plan ID.
        """
        # Validate that the associated plan exists
        plan = await self.planRepo.getById(planId)
        if not plan:
            raise NotFoundError("Plan", str(planId))
        return await self.repo.getByPlanId(planId)

    async def getRule(self, ruleId: uuid.UUID) -> BillingRule:
        """
        Retrieves details of a single billing rule record.
        """
        rule = await self.repo.getById(ruleId)
        if not rule:
            raise NotFoundError("BillingRule", str(ruleId))
        return rule

    async def updateRule(self, ruleId: uuid.UUID, data: BillingRuleUpdate) -> BillingRule:
        """
        Modifies properties of a single billing rule.
        Validates rule code uniqueness if it is modified.
        """
        rule = await self.repo.getById(ruleId)
        if not rule:
            raise NotFoundError("BillingRule", str(ruleId))
        
        # Perform validation on ruleCode if it is updated
        updateData = data.model_dump(exclude_unset=True)
        if "ruleCode" in updateData:
            code = updateData["ruleCode"]
            existing = await self.repo.getByRuleCode(rule.planId, code)
            if existing and existing.id != ruleId:
                raise ConflictError(f"Billing rule with code '{code}' already exists for this plan")
        
        result = await self.repo.update(rule, updateData)
        await self.session.commit()
        return result

    async def deleteRule(self, ruleId: uuid.UUID) -> None:
        """
        Removes a billing rule configuration.
        """
        rule = await self.repo.getById(ruleId)
        if not rule:
            raise NotFoundError("BillingRule", str(ruleId))
        await self.repo.delete(rule)
        await self.session.commit()

    async def calculateCommission(self, tenantId: uuid.UUID, orderAmount: Decimal) -> Decimal:
        """
        Calculates the commission for an order amount based on:
        - The default plan commission percent (fallback).
        - Overrides or additions defined in the BillingRule table (e.g. commission_percentage, commission_flat_fee).
        """
        # Verify tenant existence and active status
        tenant = await self.tenantRepo.getById(tenantId)
        if not tenant or not tenant.isActive:
            raise NotFoundError("Tenant", str(tenantId))

        # Check tenant plan assignment
        tenantPlan = await self.tenantPlanRepo.getByTenantId(tenantId)
        if not tenantPlan:
            # Default to 0 commission if no plan assigned
            return Decimal("0.00")

        # Resolve details of the active plan
        plan = await self.planRepo.getById(tenantPlan.planId)
        if not plan:
            return Decimal("0.00")

        # 1. Start with plan default baseline percentage
        commission_percent = plan.transactionCommissionPercent

        # 2. Check for plan-specific override percentage rule
        percentage_override = await self.repo.getByRuleCode(plan.id, "commission_percentage")
        if percentage_override and percentage_override.isActive:
            commission_percent = percentage_override.ruleValue

        # Calculate transaction percentage commission
        commission = (orderAmount * commission_percent) / Decimal("100.00")

        # 3. Add plan-specific transaction flat fee rule
        flat_fee_rule = await self.repo.getByRuleCode(plan.id, "commission_flat_fee")
        if flat_fee_rule and flat_fee_rule.isActive:
            commission += flat_fee_rule.ruleValue

        # Round to 2 decimal places precision for currency transactions
        return commission.quantize(Decimal("0.01"))

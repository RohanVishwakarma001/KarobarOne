# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/planGuard.py
# Purpose: Subscription Plan Limit Enforcement & Feature Gating
# Last updated: 2026-07-31
# ================================================================================
"""
Plan-limit enforcement service for SaaS feature gating.

Provides centralized checks for resource limits (products, services, images)
and feature access (blog, custom domain, analytics, offers, SEO score)
based on the tenant's active subscription plan.
"""

import uuid
from decimal import Decimal

import structlog
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger(__name__)


# ──────────────────────────────────────────────
# Plan Limit Constants (Free Plan)
# ──────────────────────────────────────────────
FREE_PLAN_PRODUCT_LIMIT = 6
FREE_PLAN_SERVICE_LIMIT = 6
FREE_PLAN_IMAGE_PER_PRODUCT_LIMIT = 1
FREE_PLAN_COMMISSION_PERCENT = Decimal("2.0")
PREMIUM_PLAN_COMMISSION_PERCENT = Decimal("1.0")

# Features locked on Free plan
FREE_PLAN_BLOCKED_FEATURES = {
    "blog",
    "custom_domain",
    "advanced_analytics",
    "offers_coupons",
    "seo_score",
}


class PlanLimitExceeded(HTTPException):
    """Custom exception for plan limit violations."""

    def __init__(self, resource: str, limit: int, plan: str = "Free"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "plan_limit_exceeded",
                "message": f"Your {plan} plan allows a maximum of {limit} {resource}. "
                f"Please upgrade to add more.",
                "resource": resource,
                "limit": limit,
                "plan": plan,
                "upgrade_required": True,
            },
        )


class FeatureNotAvailable(HTTPException):
    """Custom exception for feature gating violations."""

    def __init__(self, feature: str, plan: str = "Free"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "feature_not_available",
                "message": f"The '{feature}' feature is not available on your {plan} plan. "
                f"Please upgrade to unlock this feature.",
                "feature": feature,
                "plan": plan,
                "upgrade_required": True,
            },
        )


class PlanGuard:
    """
    Centralized plan-limit enforcement service.

    Checks tenant's current subscription plan and enforces resource limits
    and feature gates before allowing creation of new resources.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_tenant_plan_code(self, tenant_id: uuid.UUID) -> str | None:
        """
        Retrieves the plan code for the tenant's active subscription.

        Returns:
            The plan code string (e.g., 'free', 'starter', 'professional', 'enterprise')
            or None if no active plan is found.
        """
        try:
            from app.db.models.tenantPlanMapping import TenantPlanMapping
            from app.db.models.subscriptionPlan import SubscriptionPlan

            result = await self.db.execute(
                select(SubscriptionPlan.planCode)
                .join(
                    TenantPlanMapping,
                    TenantPlanMapping.planId == SubscriptionPlan.id,
                )
                .where(
                    TenantPlanMapping.tenantId == tenant_id,
                )
            )
            row = result.scalar_one_or_none()
            return row.lower() if row else None
        except Exception:
            return None

    def _is_free_plan(self, plan_code: str | None) -> bool:
        """Check if the plan code represents a free/starter plan."""
        if plan_code is None:
            return True  # No plan = treat as free
        return plan_code in ("free", "starter")

    async def check_product_limit(self, tenant_id: uuid.UUID) -> None:
        """
        Raises PlanLimitExceeded if tenant is on Free plan and has reached
        the maximum product count (6).

        Parameters:
            tenant_id: The tenant UUID to check against.
        """
        try:
            plan_code = await self._get_tenant_plan_code(tenant_id)
            if not self._is_free_plan(plan_code):
                return  # Unlimited products on paid plans

            from app.productsPorted.models.models import Product

            result = await self.db.execute(
                select(func.count())
                .select_from(Product)
                .where(
                    Product.tenantId == tenant_id,
                    Product.deletedAt.is_(None),
                )
            )
            count = result.scalar() or 0
            if count >= FREE_PLAN_PRODUCT_LIMIT:
                raise PlanLimitExceeded(
                    "products",
                    FREE_PLAN_PRODUCT_LIMIT,
                    f"Free plan is limited to {FREE_PLAN_PRODUCT_LIMIT} products. "
                    "Please upgrade to add more.",
                )
        except PlanLimitExceeded:
            raise
        except Exception as e:
            # Deliberately fails OPEN (doesn't block product creation) rather
            # than closed on an infra hiccup here — productsPorted runs on a
            # separate DB engine (see docs/api-mapping/catalog.md), so a
            # transient failure reaching it shouldn't break checkout/product
            # creation entirely. But it was previously a bare `except: pass`,
            # meaning that trade-off was invisible — this at least makes it
            # loud so a persistent failure (as opposed to one transient blip)
            # gets noticed instead of silently letting Free-plan limits go
            # unenforced indefinitely.
            logger.error("Product limit check failed — allowing the request through", tenantId=str(tenant_id), error=str(e))

    async def check_service_limit(self, tenant_id: uuid.UUID) -> None:
        """
        Raises PlanLimitExceeded if tenant is on Free plan and has reached
        the maximum service count (6).

        Parameters:
            tenant_id: The tenant UUID to check against.
        """
        plan_code = await self._get_tenant_plan_code(tenant_id)
        if not self._is_free_plan(plan_code):
            return

        from serviceEngine.models import Service

        result = await self.db.execute(
            select(func.count(Service.id)).where(
                Service.tenantId == tenant_id,
                Service.isActive == True,
            )
        )
        count = result.scalar() or 0

        if count >= FREE_PLAN_SERVICE_LIMIT:
            logger.warning(
                "Service limit reached",
                tenantId=str(tenant_id),
                count=count,
                limit=FREE_PLAN_SERVICE_LIMIT,
            )
            raise PlanLimitExceeded("services", FREE_PLAN_SERVICE_LIMIT)

    async def check_product_image_limit(
        self, tenant_id: uuid.UUID, product_id: uuid.UUID
    ) -> None:
        """
        Raises PlanLimitExceeded if tenant is on Free plan and the product
        already has the maximum number of images (1).

        Parameters:
            tenant_id: The tenant UUID.
            product_id: The product UUID to check image count for.
        """
        plan_code = await self._get_tenant_plan_code(tenant_id)
        if not self._is_free_plan(plan_code):
            return

        from app.productsPorted.models.models import ProductImage

        result = await self.db.execute(
            select(func.count(ProductImage.id)).where(
                ProductImage.productId == product_id,
            )
        )
        count = result.scalar() or 0

        if count >= FREE_PLAN_IMAGE_PER_PRODUCT_LIMIT:
            logger.warning(
                "Product image limit reached",
                tenantId=str(tenant_id),
                productId=str(product_id),
                count=count,
                limit=FREE_PLAN_IMAGE_PER_PRODUCT_LIMIT,
            )
            raise PlanLimitExceeded("images per product", FREE_PLAN_IMAGE_PER_PRODUCT_LIMIT)

    async def check_feature_access(
        self, tenant_id: uuid.UUID, feature_code: str
    ) -> None:
        """
        Raises FeatureNotAvailable if the requested feature is blocked
        on the tenant's current plan.

        Parameters:
            tenant_id: The tenant UUID.
            feature_code: The feature code to check (e.g., 'blog', 'custom_domain').
        """
        plan_code = await self._get_tenant_plan_code(tenant_id)
        if not self._is_free_plan(plan_code):
            return  # Paid plans have all features

        if feature_code in FREE_PLAN_BLOCKED_FEATURES:
            logger.warning(
                "Feature blocked on free plan",
                tenantId=str(tenant_id),
                feature=feature_code,
            )
            raise FeatureNotAvailable(feature_code)

    async def get_commission_rate(self, tenant_id: uuid.UUID) -> Decimal:
        """
        Returns the transaction commission rate based on the tenant's plan.

        Returns:
            Decimal: 2.0 for Free plan, 1.0 for Premium plans.
        """
        plan_code = await self._get_tenant_plan_code(tenant_id)
        if self._is_free_plan(plan_code):
            return FREE_PLAN_COMMISSION_PERCENT
        return PREMIUM_PLAN_COMMISSION_PERCENT

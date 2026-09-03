# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: api/router.py — Root API Router (Route Aggregator)
# ================================================================================
# Why this file is used:
#   - It aggregates all versioned sub-routers (v1 endpoints) into a single
#     unified APIRouter instance that is mounted in main.py.
#
# What components are inside:
#   - apiRouter  -> Central APIRouter instance consolidating routes for health, auth,
#                   tenants, brands, categories, tags, customers, users, roles,
#                   permissions, media, SEO, stores, sections, social connections,
#                   approvals, chats, invoices, and the AI blog agent.
# ================================================================================
"""
Root API router.

Aggregates all versioned sub-routers into a single router
that is included in the FastAPI app with the API prefix.
"""

from fastapi import APIRouter
from app.api.v1.endpoints.github import githubRouter
from app.api.v1.endpoints import (
    auth, health, tenantTest,
    # Brands
    brands, brandApprovals,
    # Categories
    categories,
    # Tags
    tags, tagMappings,
    # Customers
    customers, customerAddresses, customerSessions, customerGuestVerifications, customerMisc,
    # Users, Roles, Permissions, OTP, Refresh tokens, session info etc
    users, roles, permissions, loginHistory, otpVerifications, passwordResetTokens, refreshTokens,
    rolePermission, storeStaff, userRole, userSecuritySettings, userSessions,
    # Tenant & subscription
    tenants, status, plans, features, tenantPlan, planHistory, domains, tenantSettings, billingRules,
    # Media & SEO
    mediaFiles, mediaMetadata, mediaUploadLogs, mediaVariants, seoMetadata,
    # Store & website
    stores, sections, socialLinks, socialPlatforms, storeBankAccounts, websiteThemes, websiteSettings, websiteDeployments, websitePublishLogs, websiteAIContents,
    websites, adminWebsites, publicWebsite,
    # Approvals, Auditing, Versioning
    approvalRequests, entityVersions, auditLogs, statusHistory, reviewQueue,
    # Live Chat auth
    chatAuth,
    # Invoice generator
    invoice,
    # Blog Agent AI
    blogAgent
)

# Also import websocket router for chat
from app.api.v1.endpoints.chat import router as chat_ws_router
from app.api.v1.endpoints import websiteMedia

from app.api.v1.endpoints import websiteAIGeneration

from app.api.v1.endpoints import domainVerification
from app.api.v1.endpoints import cart, orders, payments
from app.api.v1.endpoints import deployment

apiRouter = APIRouter()

# ── v1 endpoints ──────────────────────────────
apiRouter.include_router(health.router)
apiRouter.include_router(auth.router)
apiRouter.include_router(tenantTest.router)

# Cart, Orders & Payments (Priority 4 — see docs/api-mapping/commerce.md)
apiRouter.include_router(cart.router)
apiRouter.include_router(orders.router)
apiRouter.include_router(payments.router)

# Brands & Approvals
apiRouter.include_router(brands.router)
apiRouter.include_router(brandApprovals.router)

# Categories
apiRouter.include_router(categories.router)

# Tags & Mappings
apiRouter.include_router(tags.router)
apiRouter.include_router(tagMappings.router)

# Customers & address, session, verification, misc
apiRouter.include_router(customers.router)
apiRouter.include_router(customerAddresses.router)
apiRouter.include_router(customerSessions.router)
apiRouter.include_router(customerGuestVerifications.guest_router)
apiRouter.include_router(customerGuestVerifications.verification_router)
apiRouter.include_router(customerMisc.activity_router)
apiRouter.include_router(customerMisc.groups_router)
apiRouter.include_router(customerMisc.notes_router)
apiRouter.include_router(customerMisc.consent_router)
apiRouter.include_router(customerMisc.password_reset_router)

# Users & Roles, Permissions, security settings, histories
apiRouter.include_router(users.router)
apiRouter.include_router(roles.router)
apiRouter.include_router(permissions.router)
apiRouter.include_router(loginHistory.router)
apiRouter.include_router(otpVerifications.router)
apiRouter.include_router(passwordResetTokens.router)
apiRouter.include_router(refreshTokens.router)
apiRouter.include_router(rolePermission.router)
apiRouter.include_router(storeStaff.router)
apiRouter.include_router(userRole.router)
apiRouter.include_router(userSecuritySettings.router)
apiRouter.include_router(userSessions.router)

# Tenant & Subscription
apiRouter.include_router(tenants.router)
apiRouter.include_router(status.router)
apiRouter.include_router(plans.router)
apiRouter.include_router(features.router)
apiRouter.include_router(tenantPlan.router)
apiRouter.include_router(planHistory.router)
apiRouter.include_router(domains.router)
apiRouter.include_router(tenantSettings.router)
apiRouter.include_router(billingRules.router)

# Media & SEO
apiRouter.include_router(mediaFiles.router)
apiRouter.include_router(mediaMetadata.router)
apiRouter.include_router(mediaUploadLogs.router)
apiRouter.include_router(mediaVariants.router)
apiRouter.include_router(seoMetadata.router)

# Store & Website
apiRouter.include_router(stores.router)
apiRouter.include_router(sections.router)
apiRouter.include_router(socialLinks.router)
apiRouter.include_router(socialPlatforms.router)
apiRouter.include_router(storeBankAccounts.router)
apiRouter.include_router(websiteThemes.router)
apiRouter.include_router(websiteSettings.router)
apiRouter.include_router(websiteDeployments.router)
apiRouter.include_router(websitePublishLogs.router)
apiRouter.include_router(websiteAIContents.router)

# Website Engine - Core Website APIs
apiRouter.include_router(websiteMedia.router)
apiRouter.include_router(websiteAIGeneration.router)
apiRouter.include_router(domainVerification.router)
apiRouter.include_router(websites.router)
apiRouter.include_router(adminWebsites.router)
apiRouter.include_router(publicWebsite.router)

# Approvals & Auditing
apiRouter.include_router(approvalRequests.router)
apiRouter.include_router(entityVersions.router)
apiRouter.include_router(auditLogs.router)
apiRouter.include_router(statusHistory.router)
apiRouter.include_router(reviewQueue.router)

# Deployment (Priority 6 — cache invalidation)
apiRouter.include_router(deployment.router)

# Live Chat (HTTP + Websocket is included in main.py directly or here)
apiRouter.include_router(chatAuth.router)
apiRouter.include_router(chat_ws_router) # Registered for ws endpoints

# Invoice
apiRouter.include_router(invoice.router)

# Blog Agent
apiRouter.include_router(blogAgent.router)
# ================================================================================
# GitHub Commerce Routes
# ================================================================================

apiRouter.include_router(githubRouter)

# Service Engine Routes (Owner - pradhansaikat123@gmail.com)
from serviceEngine.router import serviceEngineRouter
apiRouter.include_router(serviceEngineRouter)

# Customer Engine Routes (Owner - pradhansaikat123@gmail.com)
from customerEngine.router import customerEngineRouter
apiRouter.include_router(customerEngineRouter)

# Ported Products Catalog Routes
from app.productsPorted.routers.categories import router as portedCategoriesRouter
from app.productsPorted.routers.products import router as portedProductsRouter
from app.productsPorted.routers.variants import router as portedVariantsRouter
from app.productsPorted.routers.attributes import router as portedAttributesRouter
from app.productsPorted.routers.images import router as portedImagesRouter
from app.productsPorted.routers.shipping import router as portedShippingRouter
from app.productsPorted.routers.brands import router as portedBrandsRouter
from app.productsPorted.routers.variants import productVariantsRouter as portedProductVariantsRouter

apiRouter.include_router(portedCategoriesRouter, prefix="/catalog")
apiRouter.include_router(portedProductsRouter, prefix="/catalog")
apiRouter.include_router(portedVariantsRouter, prefix="/catalog")
apiRouter.include_router(portedProductVariantsRouter, prefix="/catalog")  # nested /catalog/products/{id}/variants
apiRouter.include_router(portedAttributesRouter, prefix="/catalog")
apiRouter.include_router(portedImagesRouter, prefix="/catalog")
apiRouter.include_router(portedShippingRouter, prefix="/catalog")
apiRouter.include_router(portedBrandsRouter, prefix="/catalog")
# ============================================================
# Website Engine - Additional Website Routes
# ============================================================


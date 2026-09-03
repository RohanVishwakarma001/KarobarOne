# ================================================================================
# Module: app/api/v1/endpoints/deployment.py
# Purpose: Storefront cache invalidation trigger (Priority 6)
# ================================================================================
"""
Publish-status transitions for a website already exist and are correct
(app/api/v1/endpoints/adminWebsites.py: POST /admin/websites/{approve,reject,
publish}, backed by websitePublishLogs.py) — this router only adds the piece
that was actually missing: a cache-invalidation trigger to call after a
publish, so a storefront's cached pages don't keep serving stale content.

Honesty note: this app has no cache/CDN layer wired up yet (see
app/core/redisClient.py's docstring — Redis itself is optional and, in this
deployment, unconfigured). When Redis is configured, this endpoint deletes
the matching cache keys for real. When it isn't, it still logs the
invalidation event via structlog (so the *intent* to invalidate is captured
in the deployment's logs even without a cache to act on) and reports
`cacheBackend: "none"` in its response — never a fabricated "invalidated
successfully" for a cache that doesn't exist.
"""

import uuid
from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.rbac import Roles, require_role
from app.core.redisClient import getRedisClient

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/deployment", tags=["Deployment"])


class CacheInvalidateRequest(BaseModel):
    storeId: uuid.UUID
    scope: str = Field(default="all", description="'all' or a specific cache scope, e.g. 'product', 'category', 'page'")


class CacheInvalidateResponse(BaseModel):
    storeId: uuid.UUID
    scope: str
    cacheBackend: str  # "redis" | "none"
    keysInvalidated: int
    invalidatedAt: datetime


@router.post(
    "/cache/invalidate",
    response_model=CacheInvalidateResponse,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.PLATFORM_STAFF, Roles.STORE_OWNER))],
    summary="Invalidate cached storefront pages for a store after a publish",
)
async def invalidateStorefrontCache(data: CacheInvalidateRequest) -> CacheInvalidateResponse:
    redisClient = getRedisClient()
    pattern = f"storefront:{data.storeId}:{data.scope}:*"

    if redisClient is None:
        logger.info(
            "Cache invalidation requested but no cache backend is configured — nothing to clear",
            storeId=str(data.storeId),
            scope=data.scope,
        )
        return CacheInvalidateResponse(
            storeId=data.storeId,
            scope=data.scope,
            cacheBackend="none",
            keysInvalidated=0,
            invalidatedAt=datetime.now(timezone.utc),
        )

    keysDeleted = 0
    async for key in redisClient.scan_iter(match=pattern):
        keysDeleted += await redisClient.delete(key)

    logger.info("Storefront cache invalidated", storeId=str(data.storeId), scope=data.scope, keysDeleted=keysDeleted)
    return CacheInvalidateResponse(
        storeId=data.storeId,
        scope=data.scope,
        cacheBackend="redis",
        keysInvalidated=keysDeleted,
        invalidatedAt=datetime.now(timezone.utc),
    )

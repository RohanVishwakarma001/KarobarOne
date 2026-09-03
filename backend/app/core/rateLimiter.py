# ================================================================================
# Module: app/core/rateLimiter.py
# Purpose: Per-client request rate limiting (Priority 6)
# ================================================================================
"""
RateLimitMiddleware — fixed-window rate limiting keyed by client IP.

Backed by Redis (INCR + EXPIRE) when app.core.redisClient.getRedisClient()
returns a client, so the limit is shared correctly across multiple app
instances behind a load balancer. Falls back to an in-process dict when
Redis isn't configured — correct for a single dev/staging instance, but
each instance behind a future multi-process deployment would then enforce
its own independent limit rather than a shared one. That tradeoff is
accepted (and logged once at startup, not per-request) rather than silently
pretending single-instance limiting is distributed.
"""

import time

import structlog
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import getSettings
from app.core.redisClient import getRedisClient

logger = structlog.get_logger(__name__)

# Never rate-limit health probes or the OpenAPI/docs surface — a monitoring
# system polling every few seconds shouldn't be able to trip its own limit.
_EXEMPT_PATH_PREFIXES = ("/api/v1/health", "/api/v1/docs", "/api/v1/redoc", "/api/v1/openapi.json")

_WINDOW_SECONDS = 60

# In-memory fallback: clientKey -> (windowStartEpochSeconds, count)
_localWindows: dict[str, tuple[float, int]] = {}


def _clientKey(request: Request) -> str:
    forwardedFor = request.headers.get("x-forwarded-for")
    ip = forwardedFor.split(",")[0].strip() if forwardedFor else (request.client.host if request.client else "unknown")
    return f"ratelimit:{ip}"


async def _incrementRedis(redisClient, key: str) -> int:
    count = await redisClient.incr(key)
    if count == 1:
        await redisClient.expire(key, _WINDOW_SECONDS)
    return count


def _incrementLocal(key: str) -> int:
    now = time.time()
    windowStart, count = _localWindows.get(key, (now, 0))
    if now - windowStart >= _WINDOW_SECONDS:
        windowStart, count = now, 0
    count += 1
    _localWindows[key] = (windowStart, count)
    return count


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, callNext: RequestResponseEndpoint) -> Response:
        path = request.url.path
        if any(path.startswith(p) for p in _EXEMPT_PATH_PREFIXES):
            return await callNext(request)

        settings = getSettings()
        limit = settings.rateLimitPerMinute
        key = _clientKey(request)

        redisClient = getRedisClient()
        try:
            count = await _incrementRedis(redisClient, key) if redisClient is not None else _incrementLocal(key)
        except Exception as exc:
            # A rate-limit backend hiccup should never take the whole API down.
            logger.error("Rate limiter backend error — allowing request through", error=str(exc))
            return await callNext(request)

        if count > limit:
            logger.warning("Rate limit exceeded", key=key, count=count, limit=limit)
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Too many requests. Limit is {limit} per minute.",
                    },
                },
                headers={"Retry-After": str(_WINDOW_SECONDS)},
            )

        response = await callNext(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, limit - count))
        return response

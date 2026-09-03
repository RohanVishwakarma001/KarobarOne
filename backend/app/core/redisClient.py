# ================================================================================
# Module: app/core/redisClient.py
# Purpose: Optional Redis client — used by health checks and the rate limiter
# ================================================================================
"""
Optional Redis client wrapper.

Nothing else in this codebase currently depends on Redis being present (see
app/core/tokenBlacklist.py's docstring — the token blacklist is in-memory
today). Rather than pretending Redis is wired up everywhere the Priority 6
spec mentions it, this module reports honestly: no `redisUrl` configured, or
the `redis` package not installed, means every caller gets `None` back and
falls back to its own in-process behavior (see rateLimiter.py). This mirrors
the fail-closed-not-fabricated pattern already used for Razorpay/Shiprocket/
Gemini elsewhere in app/services — a missing dependency is reported, never
silently faked as healthy.
"""

from __future__ import annotations

import time
from typing import Any

import structlog

from app.core.config import getSettings

logger = structlog.get_logger(__name__)

_client: Any = None
_clientInitialized = False


def getRedisClient() -> Any:
    """
    Return a lazily-created async Redis client, or None if Redis isn't
    configured (`redisUrl` unset) or the `redis` package isn't installed.

    Never raises — callers must treat `None` as "Redis unavailable" and
    degrade gracefully rather than erroring.
    """
    global _client, _clientInitialized

    if _clientInitialized:
        return _client
    _clientInitialized = True

    settings = getSettings()
    if not settings.redisUrl:
        logger.info("Redis not configured (redisUrl unset) — Redis-backed features run in fallback mode")
        return None

    try:
        import redis.asyncio as redisAsync
    except ImportError:
        logger.warning("REDIS_URL is set but the 'redis' package isn't installed — falling back")
        return None

    _client = redisAsync.from_url(settings.redisUrl, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)
    return _client


async def pingRedis() -> dict[str, Any]:
    """
    Health-check helper: returns a status dict, never raises.

    Shape:
      {"status": "not_configured"}                          — no client
      {"status": "healthy", "latencyMs": 3.21}               — ping succeeded
      {"status": "unhealthy", "error": "..."}                — ping failed
    """
    client = getRedisClient()
    if client is None:
        return {"status": "not_configured"}

    start = time.perf_counter()
    try:
        await client.ping()
        return {"status": "healthy", "latencyMs": round((time.perf_counter() - start) * 1000, 2)}
    except Exception as exc:
        logger.error("Redis health check failed", error=str(exc))
        return {"status": "unhealthy", "error": str(exc)}

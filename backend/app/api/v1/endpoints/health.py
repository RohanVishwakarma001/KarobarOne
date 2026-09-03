# Owner: mousamdas156@gmail.com
"""
Health check endpoints.

Provides three health check routes:
  GET /health       — Simple liveness check (no dependency checks)
  GET /health/db    — Database connectivity + connection-pool check (SELECT 1)
  GET /health/full  — Aggregate readiness: DB, Redis, and worker/Celery status

Redis and Celery: neither is actually wired into this codebase today (see
app/core/redisClient.py and app/core/tokenBlacklist.py's docstring — there is
no worker/task-queue system at all, only FastAPI's own BackgroundTasks used
in one unrelated place). /health/full reports both honestly as
"not_configured" rather than faking a green check for infrastructure that
doesn't exist yet — consistent with how this app already treats an
unconfigured Razorpay/Shiprocket/Gemini as "not configured", never as a
fabricated success.
"""

import time
from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, getSettings
from app.db.session import getDb, getEngine

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/health")
async def healthCheck(
    settings: Settings = Depends(getSettings),
) -> dict:
    """
    Liveness probe.

    Returns 200 OK if the application is running.
    Does NOT check database or external dependencies.
    """
    return {
        "status": "healthy",
        "appName": settings.appName,
        "version": settings.appVersion,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/db", response_model=None)
async def dbHealthCheck(
    db: AsyncSession = Depends(getDb),
):
    """
    Readiness probe — verifies database connectivity.

    Executes SELECT 1 against the database and reports latency.
    Returns 503 Service Unavailable if the database is unreachable.
    """
    start = time.perf_counter()
    try:
        await db.execute(text("SELECT 1"))
        latencyMs = round((time.perf_counter() - start) * 1000, 2)

        logger.info("Database health check passed", latencyMs=latencyMs)
        return {
            "status": "healthy",
            "database": "connected",
            "latencyMs": latencyMs,
            "pool": _poolStats(),
        }
    except Exception as exc:
        # Deliberately broad, not `SQLAlchemyError`: a connection-level
        # failure (DNS resolution, TCP timeout — e.g. a transient Neon DNS
        # hiccup, seen live while testing this exact endpoint) surfaces as a
        # raw socket/OS exception, not a SQLAlchemy-wrapped one, since it
        # happens during pool.connect() before SQLAlchemy's own DBAPI-error
        # translation runs. A health check that itself crashes on the one
        # failure mode it exists to detect defeats its entire purpose.
        latencyMs = round((time.perf_counter() - start) * 1000, 2)
        logger.error(
            "Database health check failed",
            error=str(exc),
            latencyMs=latencyMs,
        )
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(exc),
                "pool": _poolStats(),
            },
        )


def _poolStats() -> dict:
    """SQLAlchemy QueuePool introspection — real numbers, not estimates."""
    pool = getEngine().pool
    return {
        "size": pool.size(),
        "checkedOut": pool.checkedout(),
        "overflow": pool.overflow(),
    }


@router.get("/health/full", response_model=None)
async def fullHealthCheck(
    db: AsyncSession = Depends(getDb),
    settings: Settings = Depends(getSettings),
):
    """
    Aggregate readiness probe — database, Redis, and worker/Celery status in
    one call, the shape the internal System Health dashboard widget polls.

    Overall `status` is "healthy" only if every subsystem that IS configured
    reports healthy; an unconfigured subsystem (Redis/worker, today) doesn't
    fail the overall check — it's surfaced as "not_configured" so the
    dashboard can show it plainly rather than the endpoint lying about it.
    """
    from app.core.redisClient import pingRedis

    dbStart = time.perf_counter()
    try:
        await db.execute(text("SELECT 1"))
        dbStatus = {"status": "healthy", "latencyMs": round((time.perf_counter() - dbStart) * 1000, 2), "pool": _poolStats()}
    except Exception as exc:
        # See the matching comment on dbHealthCheck above — must catch
        # broadly, not just SQLAlchemyError, or a connection-level failure
        # crashes this endpoint instead of being reported by it.
        logger.error("Database health check failed", error=str(exc))
        dbStatus = {"status": "unhealthy", "error": str(exc), "pool": _poolStats()}

    redisStatus = await pingRedis()

    # No Celery/worker system exists in this codebase (see module docstring)
    # — reported honestly rather than faked.
    workerStatus = {"status": "not_configured"}

    subsystemStatuses = [dbStatus["status"], redisStatus["status"], workerStatus["status"]]
    overall = "unhealthy" if "unhealthy" in subsystemStatuses else "healthy"

    body = {
        "status": overall,
        "appName": settings.appName,
        "version": settings.appVersion,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "database": dbStatus,
            "redis": redisStatus,
            "worker": workerStatus,
        },
    }
    return JSONResponse(status_code=200 if overall == "healthy" else 503, content=body)

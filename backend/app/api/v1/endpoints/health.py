# Owner: mousamdas156@gmail.com
"""
Health check endpoints.

Provides two health check routes:
  GET /health     — Simple liveness check (no DB dependency)
  GET /health/db  — Database connectivity check (SELECT 1)
"""

import time
from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, getSettings
from app.db.session import getDb

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
        }
    except SQLAlchemyError as exc:
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
            },
        )

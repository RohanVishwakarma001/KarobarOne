# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/main.py
# Purpose: Application Entry Point (FastAPI Application Factory)
# Last updated: 2026-07-11
# ================================================================================
"""
FastAPI application factory.

Creates and configures the FastAPI application with:
  - Lifespan handler for startup/shutdown (DB engine lifecycle)
  - Middleware stack (CORS, Request ID, Request Timing)
  - Global exception handlers
  - Versioned API routers
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db import modelsRegistry
from app.api.router import apiRouter
from app.core.config import getSettings
from app.core.exceptions import (
    AppException,
    appExceptionHandler,
    unhandledExceptionHandler,
    validationExceptionHandler,
)
from app.core.logging import setupLogging
from app.core.middleware import RequestIDMiddleware, RequestTimingMiddleware
from app.core.tenantResolver import TenantMiddleware
from app.db.session import getEngine

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan handler.

    Purpose:
        Configures logging and manages database engine startup and shutdown.

    Parameters:
        app: The FastAPI application instance.

    Return value:
        An asynchronous iterator for the lifespan context.
    """
    # ── Startup ──
    setupLogging()
    settings = getSettings()
    logger.info(
        "Application starting",
        appName=settings.appName,
        version=settings.appVersion,
        debug=settings.debug,
    )

    yield

    # ── Shutdown ──
    logger.info("Application shutting down")
    engine = getEngine()
    await engine.dispose()
    logger.info("Database engine disposed")


def createApp() -> FastAPI:
    """
    Application factory — creates and wires up the FastAPI instance.

    Purpose:
        Creates and configures the FastAPI application with middlewares,
        exception handlers, and versioned API routers.

    Parameters:
        None

    Return value:
        A fully configured FastAPI application.
    """
    from fastapi.routing import APIRoute

    def custom_generate_unique_id(route: APIRoute) -> str:
        """
        Generate a globally unique OpenAPI operation ID.
        Uses HTTP method + route path + function name.
        """
        method = sorted(route.methods)[0].lower() if route.methods else "route"

        path = (
            route.path_format
            .strip("/")
            .replace("/", "-")
            .replace("{", "")
            .replace("}", "")
            .replace("_", "-")
        )

        return f"{method}-{path}-{route.name}"


    settings = getSettings()

    app = FastAPI(
        title=settings.appName,
        version=settings.appVersion,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=f"{settings.apiPrefix}/docs",
        redoc_url=f"{settings.apiPrefix}/redoc",
        openapi_url=f"{settings.apiPrefix}/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
    )


    # ── Middleware (order matters — outermost first) ──
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(TenantMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.corsOriginsList,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception Handlers ──
    from sqlalchemy.exc import IntegrityError
    from app.core.exceptions import valueErrorHandler, integrityErrorHandler

    app.add_exception_handler(AppException, appExceptionHandler)
    app.add_exception_handler(ValueError, valueErrorHandler)
    app.add_exception_handler(IntegrityError, integrityErrorHandler)
    app.add_exception_handler(RequestValidationError, validationExceptionHandler)
    app.add_exception_handler(Exception, unhandledExceptionHandler)

    # ── Routers ──
    app.include_router(apiRouter, prefix=settings.apiPrefix)

    # ── Serve Live Chat static UI ──
    app.mount("/chat-ui", StaticFiles(directory="app/apps/live_chat/static", html=True), name="chat-ui")

    return app


# Application instance (used by uvicorn: uvicorn app.main:app)
app = createApp()
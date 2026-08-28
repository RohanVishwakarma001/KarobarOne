# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: core/middleware.py — HTTP Middleware Stack (Request ID & Timing)
# ================================================================================
# Why this file is used:
#   - It implements middleware interceptors running globally on every incoming request.
#
# What components are inside:
#   - RequestIDMiddleware       -> Assigns/propagates transaction tracing UUIDs
#                                  and binds them to logging contexts.
#   - RequestTimingMiddleware   -> Measures execution timing and appends process
#                                  timing headers to responses.
# ================================================================================
"""
HTTP middleware stack.

RequestIDMiddleware  — Generates a unique UUID per request, attaches it to
                       structlog context and response headers (X-Request-ID).
RequestTimingMiddleware — Logs request duration and adds X-Process-Time-Ms header.
"""

import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Assign a unique request ID to every incoming request.

    If the client sends an X-Request-ID header, it is reused; otherwise a
    new UUID is generated. The ID is bound to structlog's contextvars so that
    all subsequent log lines within the request automatically include it.
    """

    async def dispatch(
        self, request: Request, callNext: RequestResponseEndpoint
    ) -> Response:
        requestId = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Clear previous request context and bind new one
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            requestId=requestId,
            method=request.method,
            path=str(request.url.path),
        )

        response = await callNext(request)
        response.headers["X-Request-ID"] = requestId
        return response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Measure and log the processing time for every request.

    Adds an X-Process-Time-Ms response header with the duration in milliseconds.
    """

    async def dispatch(
        self, request: Request, callNext: RequestResponseEndpoint
    ) -> Response:
        startTime = time.perf_counter()
        response = await callNext(request)
        durationMs = round((time.perf_counter() - startTime) * 1000, 2)

        logger.info(
            "Request completed",
            statusCode=response.status_code,
            durationMs=durationMs,
        )
        response.headers["X-Process-Time-Ms"] = str(durationMs)
        return response
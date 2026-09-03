# ================================================================================
# Module: app/core/securityHeaders.py
# Purpose: Baseline security response headers (Priority 6)
# ================================================================================
"""
SecurityHeadersMiddleware — adds the standard defensive response headers that
were previously entirely absent from this app (see app/core/middleware.py for
the existing RequestID/RequestTiming pair; this is a third, independent
middleware, not a modification of those).

Headers are the well-established OWASP secure-headers baseline. HSTS is only
sent when the request actually arrived over HTTPS (or via a
X-Forwarded-Proto: https from a TLS-terminating proxy) — sending it on a
plain-HTTP dev server would be actively wrong (it tells the browser to force
HTTPS on this host for the next year).
"""

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger(__name__)

_CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "img-src 'self' data: https:; "
    "style-src 'self' 'unsafe-inline'; "
    "script-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, callNext: RequestResponseEndpoint) -> Response:
        response = await callNext(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = _CONTENT_SECURITY_POLICY

        isHttps = request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"
        if isHttps:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response

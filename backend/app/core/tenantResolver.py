# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/tenantResolver.py
# Purpose: Tenant Resolution Strategies & Middleware
# Last updated: 2026-07-11
# ================================================================================
"""
Tenant resolution strategies and middleware.
Resolves the active tenant from incoming HTTP requests via:
  1. Custom Header (`X-Tenant-ID`)
  2. Subdomain (e.g., `tenant1.example.com`)
"""

import ipaddress
import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.exceptions import TenantNotFoundError
from app.core.tenant import resetCurrentTenantId, setCurrentTenantId

logger = structlog.get_logger(__name__)

# Subdomains that should NOT be treated as tenant slugs
blacklistedSubdomains = {"www", "api", "localhost", "admin", "mail", "portal", "dashboard"}


def isIpAddress(host: str) -> bool:
    """
    Check if the host string is a valid IP address (v4 or v6).

    Purpose:
        Validates if the provided host string represents an IP address.

    Parameters:
        host: Host string to check.

    Return value:
        True if the host is a valid IP, False otherwise.
    """
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def resolveTenantFromRequest(request: Request) -> str | None:
    """
    Resolve tenant ID/slug from the HTTP Request.

    Purpose:
        Extracts the tenant ID from custom headers or subdomain logic.

    Parameters:
        request: The FastAPI/Starlette Request instance.

    Return value:
        The resolved tenant ID slug or None.
    """
    # 1. Custom Header strategy (highest priority)
    tenantId = request.headers.get("X-Tenant-ID")
    if tenantId:
        return tenantId

    # 2. Subdomain strategy
    host = request.headers.get("host", "")
    # Strip port if present (e.g. localhost:8000)
    if ":" in host:
        host = host.split(":")[0]

    # If host is an IP address (e.g., 127.0.0.1), subdomain routing is not applicable
    if isIpAddress(host):
        return None

    parts = host.split(".")
    # If the host is tenant1.example.com -> ['tenant1', 'example', 'com']
    # If the host is tenant1.localhost -> ['tenant1', 'localhost']
    if len(parts) > 1:
        subdomain = parts[0].lower()
        if subdomain not in blacklistedSubdomains:
            return subdomain

    return None


def getTenantId(request: Request) -> str:
    """
    FastAPI dependency to extract and assert tenant presence.

    Purpose:
        FastAPI route dependency that extracts and validates the tenant ID.

    Parameters:
        request: The Request instance.

    Return value:
        The active tenant ID slug.

    Exceptions:
        TenantNotFoundError: If the tenant cannot be resolved.
    """
    tenantId = resolveTenantFromRequest(request)
    if not tenantId:
        logger.warning("Tenant resolution failed for request", path=request.url.path)
        raise TenantNotFoundError("Could not resolve tenant from X-Tenant-ID header or subdomain")
    return tenantId


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically intercepts requests, resolves the tenant context,
    sets the contextvars variable, and binds it to logging.
    """

    async def dispatch(self, request: Request, callNext: RequestResponseEndpoint) -> Response:
        """
        Intercepts and resolves tenant ID, setting the request context variables.

        Purpose:
            Middleware dispatch hook that binds the tenant context to logging and ContextVar.

        Parameters:
            request: Incoming HTTP Request.
            callNext: The next middleware endpoint/route handler.

        Return value:
            The HTTP Response.
        """
        structlog.contextvars.clear_contextvars()
        tenantId = resolveTenantFromRequest(request)

        # Bind tenant context to structlog request logging
        if tenantId:
            structlog.contextvars.bind_contextvars(tenantId=tenantId)
            logger.debug("Tenant context resolved", tenantId=tenantId)

        # Set the request-scoped ContextVar
        token = setCurrentTenantId(tenantId)
        try:
            response = await callNext(request)

            # Include resolved tenant in response headers for transparency/client utility
            if tenantId:
                response.headers["X-Tenant-ID"] = tenantId

            return response
        finally:
            resetCurrentTenantId(token)
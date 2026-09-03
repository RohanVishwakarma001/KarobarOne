# ================================================================================
# Module: app/core/auditMiddleware.py
# Purpose: Automatic background audit-log writes for admin mutations (Priority 6)
# ================================================================================
"""
AuditLogMiddleware — the AuditLog model + /audit-logs router already existed
and are correct (app/db/models/approvals.py::AuditLog, already fixed for the
camelCase-tablename bug this session hit repeatedly — see that file's
comment). What was missing is anything that actually WRITES to it: the only
existing writer was the manual `POST /audit-logs` endpoint. This middleware
closes that gap by logging every successful mutating request automatically,
without any route needing to opt in.

Scope, deliberately: this captures IP address, user agent, actor, method,
path-derived entity type/id, and the raw request body as `newValue` — it does
NOT attempt a real before/after field diff (`oldValue`/`changedFields` are
left null), because computing that correctly requires route-specific
knowledge of what changed, which a generic middleware can't have. A per-route
diff is a separate, larger feature than "log admin mutations automatically."

Runs as fire-and-forget: the DB write happens in a background asyncio task on
its own session (the request's own DB session is already closed by the time
middleware post-processing runs, since BaseHTTPMiddleware's callNext awaits
the full route handler including dependency cleanup), so a slow or failed
audit write never adds latency to, or breaks, the actual response.
"""

import asyncio
import json
import re
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import getSettings

logger = structlog.get_logger(__name__)

_MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

# Never audit-log auth (credentials in the body), health probes, or the
# audit-log endpoint itself (would recurse into logging its own POST calls).
_EXEMPT_PATH_PREFIXES = ("/api/v1/health", "/api/v1/auth", "/api/v1/audit-logs", "/api/v1/docs", "/api/v1/openapi.json")

_METHOD_TO_ACTION_TYPE = {"POST": "CREATE", "PUT": "UPDATE", "PATCH": "UPDATE", "DELETE": "DELETE"}

_UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)

_NIL_UUID = uuid.UUID(int=0)


def _extractEntityType(path: str) -> str:
    """First non-UUID, non-empty path segment after the API prefix, e.g. '/api/v1/tenants/{id}/plan' -> 'tenants'."""
    settings = getSettings()
    trimmed = path.removeprefix(settings.apiPrefix).strip("/")
    segments = [s for s in trimmed.split("/") if s and not _UUID_RE.fullmatch(s)]
    return (segments[0] if segments else "unknown")[:50]


def _extractEntityId(path: str) -> uuid.UUID:
    match = _UUID_RE.search(path)
    return uuid.UUID(match.group(0)) if match else _NIL_UUID


def _extractPerformedBy(authHeader: str | None) -> uuid.UUID | None:
    if not authHeader or not authHeader.lower().startswith("bearer "):
        return None
    try:
        from app.core.security import decodeToken

        payload = decodeToken(authHeader.split(" ", 1)[1])
        subject = payload.get("sub")
        return uuid.UUID(str(subject)) if subject else None
    except Exception:
        # Audit logging must never fail a request over an expired/invalid
        # token — the route's own auth dependency is the real enforcement
        # point; this is best-effort attribution only.
        return None


def _extractClientIp(request: Request) -> str | None:
    forwardedFor = request.headers.get("x-forwarded-for")
    if forwardedFor:
        return forwardedFor.split(",")[0].strip()
    return request.client.host if request.client else None


async def _writeAuditLogEntry(
    *,
    tenantId: uuid.UUID | None,
    entityType: str,
    entityId: uuid.UUID,
    actionType: str,
    newValue: dict | list | None,
    performedBy: uuid.UUID | None,
    ipAddress: str | None,
    userAgent: str | None,
) -> None:
    from app.db.models.approvals import AuditLog
    from app.db.session import getSessionFactory

    sessionFactory = getSessionFactory()
    async with sessionFactory() as session:
        try:
            session.add(
                AuditLog(
                    tenantId=tenantId,
                    entityType=entityType,
                    entityId=entityId,
                    actionType=actionType,
                    newValue=newValue,
                    performedBy=performedBy,
                    ipAddress=ipAddress,
                    userAgent=userAgent,
                )
            )
            await session.commit()
        except Exception as exc:
            await session.rollback()
            logger.error("Background audit-log write failed", error=str(exc), entityType=entityType, actionType=actionType)


def _logTaskException(task: asyncio.Task) -> None:
    """`asyncio.create_task`'s exceptions are swallowed unless retrieved — surface them via structlog instead of losing them silently."""
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        logger.error("Background audit-log task raised", error=str(exc))


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, callNext: RequestResponseEndpoint) -> Response:
        path = request.url.path
        shouldAudit = request.method in _MUTATING_METHODS and not any(path.startswith(p) for p in _EXEMPT_PATH_PREFIXES)

        bodyBytes = await request.body() if shouldAudit else b""
        response = await callNext(request)

        if shouldAudit and response.status_code < 400:
            newValue: dict | list | None = None
            if bodyBytes:
                try:
                    newValue = json.loads(bodyBytes)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    newValue = None

            tenantIdHeader = request.headers.get("x-tenant-id")
            try:
                tenantId = uuid.UUID(tenantIdHeader) if tenantIdHeader else None
            except ValueError:
                tenantId = None

            task = asyncio.create_task(
                _writeAuditLogEntry(
                    tenantId=tenantId,
                    entityType=_extractEntityType(path),
                    entityId=_extractEntityId(path),
                    actionType=_METHOD_TO_ACTION_TYPE[request.method],
                    newValue=newValue,
                    performedBy=_extractPerformedBy(request.headers.get("authorization")),
                    ipAddress=_extractClientIp(request),
                    userAgent=request.headers.get("user-agent"),
                )
            )
            task.add_done_callback(_logTaskException)

        return response

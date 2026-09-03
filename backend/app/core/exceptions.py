# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/exceptions.py
# Purpose: Global Exception Hierarchy & Handlers
# Last updated: 2026-07-11
# ================================================================================
"""
Global exception handling.

Defines a custom exception hierarchy and FastAPI exception handlers that
produce consistent, structured error responses.

Error response schema:
{
    "success": false,
    "error": {
        "code": "NOT_FOUND",
        "message": "Resource not found",
        "details": [...]   # only for validation errors
    }
}

All errors are logged with full context (request_id, path, method) via structlog.
Stack traces are NEVER leaked to clients.
"""

import structlog
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = structlog.get_logger(__name__)


# ──────────────────────────────────────────────
# Custom Exception Hierarchy
# ──────────────────────────────────────────────


class AppException(Exception):
    """Base application exception. All custom exceptions inherit from this."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        statusCode: int = 500,
        errorCode: str = "INTERNAL_ERROR",
    ) -> None:
        self.message = message
        self.statusCode = statusCode
        self.errorCode = errorCode
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found (404)."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message=message, statusCode=404, errorCode="NOT_FOUND")


class TenantNotFoundError(NotFoundError):
    """Tenant workspace not found (404)."""

    def __init__(self, message: str = "Tenant not found or inactive") -> None:
        super().__init__(message=message)
        self.errorCode = "TENANT_NOT_FOUND"


class BadRequestError(AppException):
    """Invalid client request (400)."""

    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(message=message, statusCode=400, errorCode="BAD_REQUEST")


class ConflictError(AppException):
    """Resource conflict / duplicate (409)."""

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(message=message, statusCode=409, errorCode="CONFLICT")


class UnauthorizedError(AppException):
    """Authentication required (401)."""

    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(message=message, statusCode=401, errorCode="UNAUTHORIZED")


class TokenExpiredError(UnauthorizedError):
    """Token has expired (401)."""

    def __init__(self, message: str = "Token has expired") -> None:
        super().__init__(message=message)
        self.errorCode = "TOKEN_EXPIRED"


class TokenInvalidError(UnauthorizedError):
    """Token is invalid or malformed (401)."""

    def __init__(self, message: str = "Token is invalid") -> None:
        super().__init__(message=message)
        self.errorCode = "TOKEN_INVALID"


class ForbiddenError(AppException):
    """Insufficient permissions (403)."""

    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(message=message, statusCode=403, errorCode="FORBIDDEN")


# ──────────────────────────────────────────────
# Exception Handlers (registered in main.py)
# ──────────────────────────────────────────────


async def appExceptionHandler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle all AppException subclasses with a structured error response.

    Purpose:
        Custom exception handler for domain/application level errors.

    Parameters:
        request: The incoming Request instance.
        exc: The AppException instance.

    Return value:
        JSONResponse with structured error information and appropriate status code.
    """
    logger.error(
        "Application error",
        errorCode=exc.errorCode,
        statusCode=exc.statusCode,
        message=exc.message,
        path=str(request.url),
        method=request.method,
    )
    return JSONResponse(
        status_code=exc.statusCode,
        content={
            "success": False,
            "error": {
                "code": exc.errorCode,
                "message": exc.message,
            },
        },
    )


async def validationExceptionHandler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic/FastAPI validation errors with field-level details.

    Purpose:
        Custom exception handler for RequestValidationError exceptions.

    Parameters:
        request: The incoming Request instance.
        exc: The validation error details.

    Return value:
        JSONResponse containing field validation details with status code 422.
    """
    logger.warning(
        "Validation error",
        path=str(request.url),
        method=request.method,
        errors=exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": _sanitizeValidationErrors(exc.errors()),
            },
        },
    )


def _sanitizeValidationErrors(errors: list[dict]) -> list[dict]:
    """
    pydantic's error dicts can carry a live exception instance under
    ctx.error (e.g. a raw ValueError raised by a @field_validator) — that's
    not JSON-serializable, which crashes this handler outright (a 500
    instead of the intended 422). Stringify it instead.
    """
    sanitized = []
    for err in errors:
        err = dict(err)
        ctx = err.get("ctx")
        if isinstance(ctx, dict) and isinstance(ctx.get("error"), BaseException):
            err["ctx"] = {**ctx, "error": str(ctx["error"])}
        sanitized.append(err)
    return sanitized


async def unhandledExceptionHandler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Catch-all handler for unexpected exceptions.

    Purpose:
        Handles any unexpected or unhandled exception securely by masking details.

    Parameters:
        request: The incoming Request instance.
        exc: The generic exception.

    Return value:
        JSONResponse with status code 500.
    """
    logger.exception(
        "Unhandled exception",
        path=str(request.url),
        method=request.method,
        excType=type(exc).__name__,
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
        },
    )


async def valueErrorHandler(
    request: Request, exc: ValueError
) -> JSONResponse:
    """Handle ValueError gracefully as a 400 Bad Request."""
    logger.warning(
        "ValueError handled",
        path=str(request.url),
        method=request.method,
        detail=str(exc),
    )
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "BAD_REQUEST",
                "message": str(exc),
            },
        },
    )


async def integrityErrorHandler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle SQLAlchemy IntegrityError gracefully as a 409 Conflict."""
    logger.warning(
        "IntegrityError handled",
        path=str(request.url),
        method=request.method,
        detail=str(exc),
    )
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": {
                "code": "CONFLICT",
                "message": "Database constraint violation. A related record may not exist or a duplicate exists.",
            },
        },
    )
# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: core/dependencies.py — Shared FastAPI Dependencies (Auth)
# ================================================================================
# Why this file is used:
#   - Declares common authentication parameters utilized across route layers.
#
# What components are inside:
#   - securityScheme     -> Bearer security token schema container.
#   - getCurrentUserId() -> Resolves and validates Bearer access tokens to return user ID.
# ================================================================================
"""
Shared FastAPI dependencies.
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decodeToken

# Reusable security scheme for Bearer token auth in Swagger UI
securityScheme = HTTPBearer(auto_error=True)


async def getCurrentUserId(
    credentials: HTTPAuthorizationCredentials = Depends(securityScheme),
) -> str:
    """
    FastAPI dependency to authenticate requests using JWT access tokens.

    Extracts the token from the Authorization header, decodes and validates it,
    and returns the subject (user ID) from the token.

    Raises:
        TokenExpiredError: If the token has expired
        TokenInvalidError: If the token is invalid, malformed, or of incorrect type
    """
    token = credentials.credentials
    payload = decodeToken(token, expectedType="access")
    return payload["sub"]


async def getCurrentUserWithRole(
    credentials: HTTPAuthorizationCredentials = Depends(securityScheme),
) -> dict:
    """
    FastAPI dependency to authenticate requests and return full user context.

    Extracts the token from the Authorization header, decodes and validates it,
    and returns the user context dict containing userId, role, and tenantId.

    Returns:
        dict with keys: userId (str), role (str|None), tenantId (str|None)

    Raises:
        TokenExpiredError: If the token has expired
        TokenInvalidError: If the token is invalid, malformed, or of incorrect type
    """
    token = credentials.credentials
    payload = decodeToken(token, expectedType="access")
    return {
        "userId": payload["sub"],
        "role": payload.get("role"),
        "tenantId": payload.get("tenantId"),
    }
# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/security.py
# Purpose: JWT Token Generation & Validation
# Last updated: 2026-07-11
# ================================================================================
"""
Security utilities for JWT token generation and validation.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
import structlog

from app.core.config import getSettings
from app.core.exceptions import TokenExpiredError, TokenInvalidError
from app.core.tokenBlacklist import is_revoked

logger = structlog.get_logger(__name__)


def createToken(
    subject: str | Any,
    expiresDelta: timedelta,
    tokenType: str,
    role: str | None = None,
    tenantId: str | None = None,
) -> str:
    """
    Generate a signed JWT token.

    Purpose:
        Generates and signs a JWT token with custom subject, duration, and type.

    Parameters:
        subject: The subject of the token (e.g. user ID).
        expiresDelta: Expiry duration.
        tokenType: The type of token ("access" or "refresh").

    Return value:
        The encoded JWT token string.

    Exceptions:
        TokenInvalidError: If the token encoding fails.
    """
    settings = getSettings()
    now = datetime.now(timezone.utc)
    expire = now + expiresDelta

    jti = str(uuid.uuid4())
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": tokenType,
        "role": role,
        "tenantId": tenantId,
        "jti": jti,
    }

    try:
        encodedJwt = jwt.encode(
            payload,
            settings.jwtSecretKey,
            algorithm=settings.jwtAlgorithm,
        )
        return encodedJwt
    except Exception as exc:
        logger.exception("Failed to encode JWT token", subject=subject, tokenType=tokenType)
        raise TokenInvalidError("Failed to generate token") from exc


def createAccessToken(
    subject: str | Any,
    expiresDelta: timedelta | None = None,
    role: str | None = None,
    tenantId: str | None = None,
) -> str:
    """
    Create a JWT access token.

    Purpose:
        Generates a short-lived user access token.

    Parameters:
        subject: The subject of the token.
        expiresDelta: Optional custom expiry duration.

    Return value:
        The encoded access token string.
    """
    settings = getSettings()
    if expiresDelta is None:
        expiresDelta = timedelta(minutes=settings.accessTokenExpireMinutes)
    return createToken(subject, expiresDelta, tokenType="access", role=role, tenantId=tenantId)


def createRefreshToken(
    subject: str | Any,
    expiresDelta: timedelta | None = None,
    role: str | None = None,
    tenantId: str | None = None,
) -> str:
    """
    Create a JWT refresh token.

    Purpose:
        Generates a long-lived user refresh token.

    Parameters:
        subject: The subject of the token.
        expiresDelta: Optional custom expiry duration.

    Return value:
        The encoded refresh token string.
    """
    settings = getSettings()
    if expiresDelta is None:
        expiresDelta = timedelta(days=settings.refreshTokenExpireDays)
    return createToken(subject, expiresDelta, tokenType="refresh", role=role, tenantId=tenantId)


def decodeToken(token: str, expectedType: str | None = None) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Purpose:
        Decodes and verifies a JWT token.

    Parameters:
        token: The raw JWT string.
        expectedType: Optional expected token type ("access" or "refresh").

    Return value:
        The decoded payload dict.

    Exceptions:
        TokenExpiredError: If the token signature is expired.
        TokenInvalidError: If the token is invalid, malformed, or mismatching type.
    """
    settings = getSettings()
    try:
        payload = jwt.decode(
            token,
            settings.jwtSecretKey,
            algorithms=[settings.jwtAlgorithm],
        )

        # Check token revocation
        jti = payload.get("jti")
        if jti and is_revoked(jti):
            logger.warning("Revoked token presented", jti=jti)
            raise TokenInvalidError("Token has been revoked")

        # Validate token type if expected
        if expectedType and payload.get("type") != expectedType:
            logger.warning("Token type mismatch", actual=payload.get("type"), expected=expectedType)
            raise TokenInvalidError(f"Invalid token type. Expected {expectedType} token.")

        return payload
    except jwt.ExpiredSignatureError as exc:
        logger.warning("JWT token expired", tokenType=expectedType)
        raise TokenExpiredError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        logger.warning("Invalid JWT token", error=str(exc))
        raise TokenInvalidError("Token is invalid or malformed") from exc
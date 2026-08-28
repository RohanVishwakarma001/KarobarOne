# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/tokenBlacklist.py
# Purpose: JWT Token Revocation Tracking
# Last updated: 2026-07-31
# ================================================================================
"""
In-memory token blacklist for tracking revoked JWT tokens.

Provides functions to revoke tokens (e.g., on logout) and check
if a token has been revoked before allowing access.

Note: In production, this should be replaced with Redis or a
database-backed solution for persistence across restarts.
"""

import threading
from datetime import datetime, timezone

import structlog

logger = structlog.get_logger(__name__)

# Thread-safe set of revoked token JTIs
_revoked_jtis: set[str] = set()
_lock = threading.Lock()


def revoke_token(jti: str) -> None:
    """
    Add a JWT ID (jti) to the revocation blacklist.

    Purpose:
        Marks a token as revoked so it cannot be used for further authentication.
        Called during logout or forced session termination.

    Parameters:
        jti: The unique JWT ID claim from the token to revoke.
    """
    with _lock:
        _revoked_jtis.add(jti)
    logger.info("Token revoked", jti=jti)


def is_revoked(jti: str) -> bool:
    """
    Check if a JWT ID (jti) has been revoked.

    Purpose:
        Verifies whether a token is still valid by checking the blacklist.
        Called during token decoding/validation.

    Parameters:
        jti: The unique JWT ID claim from the token to check.

    Return value:
        True if the token has been revoked, False otherwise.
    """
    with _lock:
        return jti in _revoked_jtis


def get_revoked_count() -> int:
    """
    Get the number of currently revoked tokens.

    Purpose:
        Utility function for monitoring/debugging.

    Return value:
        The count of revoked JTIs in the blacklist.
    """
    with _lock:
        return len(_revoked_jtis)


def clear_expired_tokens() -> None:
    """
    Placeholder for periodic cleanup of expired tokens from the blacklist.

    Purpose:
        In a production system, this would remove JTIs whose corresponding
        tokens have already expired (since expired tokens are rejected
        regardless of blacklist status).
    """
    # TODO: Implement cleanup based on token expiry timestamps
    pass

# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/tenant.py
# Purpose: Request-Scoped Tenant Context (ContextVar)
# Last updated: 2026-07-11
# ================================================================================
"""
ContextVar container for managing request-scoped tenant context.
Allows downstream layers (database, services) to retrieve the active tenant
without passing it as function arguments.
"""

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar, Token

# Request-scoped variable holding the active tenant ID/slug
_currentTenantId: ContextVar[str | None] = ContextVar("currentTenantId", default=None)


def getCurrentTenantId() -> str | None:
    """
    Retrieve the tenant ID for the current request context.

    Purpose:
        Retrieves the tenant ID for the current request context.

    Parameters:
        None

    Return value:
        The current tenant ID string, or None if no tenant is set.
    """
    return _currentTenantId.get()


def setCurrentTenantId(tenantId: str | None) -> Token[str | None]:
    """
    Set the tenant ID for the current request context.

    Purpose:
        Sets the tenant ID for the current request context and returns a reset Token.

    Parameters:
        tenantId: The tenant ID string or None to clear.

    Return value:
        A Token that can be used to reset the context variable.
    """
    return _currentTenantId.set(tenantId)


def resetCurrentTenantId(token: Token[str | None]) -> None:
    """
    Reset the tenant ID context variable back to its previous state.

    Purpose:
        Resets the tenant ID context variable back to its previous state using the Token.

    Parameters:
        token: The Token returned by setCurrentTenantId.

    Return value:
        None
    """
    _currentTenantId.reset(token)


@contextmanager
def tenantContext(tenantId: str | None) -> Generator[None, None, None]:
    """
    Context manager to execute a block of code with a specific tenant ID.

    Purpose:
        Executes a block of code within a context manager with a specific tenant ID.

    Parameters:
        tenantId: The tenant ID string or None.

    Return value:
        A generator yielding None.
    """
    token = setCurrentTenantId(tenantId)
    try:
        yield
    finally:
        resetCurrentTenantId(token)
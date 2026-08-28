# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: core/exceptionsCompat.py — Exception Compatibility Layer
# ================================================================================
# Why this file is used:
#   - It adapts base exceptions to match legacy application signatures.
#
# What components are inside:
#   - NotFoundError          -> Extends base NotFoundError with argument helpers.
#   - ConflictError          -> Extends base ConflictError with signature adapters.
#   - BusinessValidationError -> Raised when actions violate custom business constraints.
# ================================================================================
"""
Compatibility layer for custom exceptions defined in modular apps.
"""

from app.core.exceptions import (
    NotFoundError as FoundationNotFoundError,
    ConflictError as FoundationConflictError,
    BadRequestError as FoundationBadRequestError,
    UnauthorizedError as FoundationUnauthorizedError,
)

class NotFoundError(FoundationNotFoundError):
    """Raised when a requested resource does not exist (argument compatibility)."""
    def __init__(self, resource: str, identifier: str | None = None):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with id '{identifier}' not found"
        super().__init__(message)

class ConflictError(FoundationConflictError):
    """Raised when a resource already exists or conflicts with another."""
    def __init__(self, detail: str):
        super().__init__(detail)

class BusinessValidationError(Exception):
    """Raised when a business rule is violated."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

class AuthenticationError(FoundationUnauthorizedError):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "Invalid email or password"):
        self.detail = detail
        super().__init__(message=detail)

class AccountLockedError(FoundationUnauthorizedError):
    """Raised when an account is locked due to excessive failed login attempts."""
    def __init__(self, detail: str = "Account is locked due to too many failed login attempts"):
        self.detail = detail
        super().__init__(message=detail)
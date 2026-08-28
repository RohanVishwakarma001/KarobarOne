# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/rbac.py
# Purpose: Role-Based Access Control Dependencies
# Last updated: 2026-07-31
# ================================================================================
"""
RBAC dependency utilities for FastAPI route protection.
Provides reusable dependencies to enforce role-based and permission-based
access control on API endpoints.
"""

import uuid
from typing import Any, Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import getCurrentUserWithRole
from app.db.session import getDb


# ──────────────────────────────────────────────
# Role Constants
# ──────────────────────────────────────────────

class Roles:
    """System-wide role identifiers."""
    PLATFORM_OWNER = "platform_owner"
    PLATFORM_STAFF = "platform_staff"
    STORE_OWNER = "store_owner"
    STORE_ADMIN = "store_admin"
    STAFF = "staff"
    CUSTOMER = "customer"


# ──────────────────────────────────────────────
# Role Guard Dependency
# ──────────────────────────────────────────────

def require_role(*allowed_roles: str) -> Callable:
    """
    FastAPI dependency factory that enforces role-based access control.

    Usage:
        @router.post("/", dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))])
        async def create_tenant(...):
            ...

    Parameters:
        *allowed_roles: One or more role strings that are permitted to access the endpoint.

    Returns:
        A FastAPI dependency function.
    """
    async def _role_guard(
        current_user: dict = Depends(getCurrentUserWithRole),
    ) -> dict:
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {', '.join(allowed_roles)}. Your role: {user_role}",
            )
        return current_user
    return _role_guard


# ──────────────────────────────────────────────
# Tenant Ownership Guard
# ──────────────────────────────────────────────

def require_tenant_match(tenant_id_param: str = "tenantId") -> Callable:
    """
    FastAPI dependency factory ensuring the authenticated user belongs to
    the tenant specified in the path parameter.

    Platform-level roles (platform_owner, platform_staff) bypass this check.

    Usage:
        @router.patch("/{tenantId}/settings", dependencies=[Depends(require_tenant_match())])
    """
    from fastapi import Request

    async def _tenant_guard(
        request: Request,
        current_user: dict = Depends(getCurrentUserWithRole),
    ) -> dict:
        user_role = current_user.get("role")
        # Platform-level roles can access any tenant
        if user_role in (Roles.PLATFORM_OWNER, Roles.PLATFORM_STAFF):
            return current_user

        # Extract tenantId from path parameters
        path_tenant_id = request.path_params.get(tenant_id_param)
        user_tenant_id = current_user.get("tenantId")

        if not path_tenant_id or not user_tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tenant context is required for this operation.",
            )

        if str(path_tenant_id) != str(user_tenant_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You do not belong to this tenant.",
            )
        return current_user
    return _tenant_guard


# ──────────────────────────────────────────────
# Permission Guard (for store-staff fine-grained permissions)
# ──────────────────────────────────────────────

def require_permission(permission_code: str) -> Callable:
    """
    FastAPI dependency factory for fine-grained store-staff permission checks.

    Checks if the user's assigned store-staff permissions include the
    specified permission code. Platform roles and store_owner/store_admin
    bypass this check (they have implicit full access).

    Usage:
        @router.post("/products/", dependencies=[Depends(require_permission("manage_products"))])
    """
    async def _permission_guard(
        current_user: dict = Depends(getCurrentUserWithRole),
        db: AsyncSession = Depends(getDb),
    ) -> dict:
        user_role = current_user.get("role")

        # These roles have implicit full access
        bypass_roles = (
            Roles.PLATFORM_OWNER,
            Roles.PLATFORM_STAFF,
            Roles.STORE_OWNER,
            Roles.STORE_ADMIN,
        )
        if user_role in bypass_roles:
            return current_user

        # For staff role, check store-specific permissions
        user_id = current_user.get("userId")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User identity could not be resolved.",
            )

        # Query the StoreStaffPermission table
        from app.db.models.storeStaffPermission import StoreStaffPermission
        from app.db.models.permission import Permission

        result = await db.execute(
            select(Permission.code)
            .join(
                StoreStaffPermission,
                StoreStaffPermission.permissionId == Permission.id,
            )
            .where(
                StoreStaffPermission.userId == uuid.UUID(str(user_id)),
                StoreStaffPermission.deletedAt.is_(None),
            )
        )
        user_permissions = {row[0] for row in result.fetchall()}

        if permission_code not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required permission: '{permission_code}'.",
            )
        return current_user
    return _permission_guard

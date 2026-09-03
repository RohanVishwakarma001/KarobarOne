# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for rolePermissionMapping.
Defines the database schema, table columns, constraints, and relationships for rolePermissionMapping.
"""

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


# --------------------------------------------------------------------------------
# RolePermissionMapping Model
# Many-to-many mapping linking roles to the permissions they are granted.
# Uses 'BaseModel' to automatically include a 'createdAt' timestamp.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class RolePermissionMapping(BaseModel):
    # Real table is camelCase ("rolePermissionMapping") — see the matching
    # note on TenantPlanHistory's __tablename__ for the recurring pattern.
    __tablename__ = "rolePermissionMapping"

    # UniqueConstraint: Prevents granting the same permission to a role more than once.
    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permission",
        ),
    )

    # roleId: The role being granted the permission.
    # ondelete="CASCADE" removes mapping automatically if the role is deleted.
    roleId: Mapped[uuid.UUID] = mapped_column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey(
            "roles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # permissionId: The permission being granted to the role.
    # ondelete="CASCADE" removes mapping automatically if the permission is deleted.
    permissionId: Mapped[uuid.UUID] = mapped_column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey(
            "permissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # role: Relationship back to the related Role record.
    role = relationship(
        "Role",
        back_populates="permissionMappings",
    )

    # permission: Relationship back to the related Permission record.
    permission = relationship(
        "Permission",
        back_populates="roleMappings",
    )

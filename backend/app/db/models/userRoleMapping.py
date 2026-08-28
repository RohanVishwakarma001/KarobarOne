# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for userRoleMapping.
Defines the database schema, table columns, constraints, and relationships for userRoleMapping.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# UserRoleMapping Model
# Assigns roles to users, supporting multi-role and tenant-scoped role assignment.
# Uses 'BaseUUID' since the audit timestamp here is 'assignedAt', not 'createdAt'.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class UserRoleMapping(BaseUUID):
    __tablename__ = "user_role_mapping"

    # UniqueConstraint: Prevents assigning the same role twice to a user within the same tenant scope.
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "role_id",
            "tenant_id",
            name="uq_user_role_tenant",
        ),
    )

    # userId: The user receiving the role assignment.
    # ondelete="CASCADE" removes the mapping automatically if the user is deleted.
    userId: Mapped[uuid.UUID] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # roleId: The role being assigned.
    # ondelete="CASCADE" removes the mapping automatically if the role is deleted.
    roleId: Mapped[uuid.UUID] = mapped_column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey(
            "roles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # tenantId: Optional tenant scope for the role assignment (NULL means global/platform-wide role).
    tenantId: Mapped[uuid.UUID | None] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        ForeignKey("tenants_details.id"),
        nullable=True,
    )

    # assignedBy: UUID of the user who performed the assignment (optional, e.g. system-assigned).
    assignedBy: Mapped[uuid.UUID | None] = mapped_column(
        "assigned_by",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # assignedAt: Timestamp when the role assignment took place.
    assignedAt: Mapped[datetime] = mapped_column(
        "assigned_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # user: Relationship back to the assigned User record.
    user = relationship(
        "User",
        back_populates="roleMappings",
        foreign_keys=[userId],
    )

    # role: Relationship back to the assigned Role record.
    role = relationship(
        "Role",
        back_populates="userMappings",
        foreign_keys=[roleId],
    )

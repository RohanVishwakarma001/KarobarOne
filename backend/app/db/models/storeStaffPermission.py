# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for storeStaffPermission.
Defines the database schema, table columns, constraints, and relationships for storeStaffPermission.
"""

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


# --------------------------------------------------------------------------------
# StoreStaffPermission Model
# Fine-grained permission overrides granted to a user at a specific store level.
# Uses 'BaseModel' to automatically include a 'createdAt' timestamp.
# Python attribute names are camelCase; DB column names stay snake_case.
#
# NOTE: 'storeId' is left as a plain UUID column (no ForeignKey constraint) since
# the 'stores' table is not yet part of this module. Add the FK once M3's stores
# table is available in this service's metadata.
# --------------------------------------------------------------------------------
class StoreStaffPermission(BaseModel):
    __tablename__ = "store_staff_permissions"

    # UniqueConstraint: Prevents granting the same permission twice to a user at the same store.
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "store_id",
            "permission_id",
            name="uq_user_store_permission",
        ),
    )

    # userId: The staff member receiving the store-level permission override.
    # ondelete="CASCADE" removes the override automatically if the user is deleted.
    userId: Mapped[uuid.UUID] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # storeId: The store this permission override applies to (no FK; stores table is external).
    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        nullable=False,
    )

    # permissionId: The permission being granted at the store level.
    # ondelete="CASCADE" removes the override automatically if the permission is deleted.
    permissionId: Mapped[uuid.UUID] = mapped_column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey(
            "permissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # grantedBy: UUID of the user who granted this override (optional).
    grantedBy: Mapped[uuid.UUID | None] = mapped_column(
        "granted_by",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # user: Relationship back to the related User record.
    user = relationship(
        "User",
        back_populates="storePermissions",
        foreign_keys=[userId],
    )

    # permission: Relationship back to the related Permission record.
    permission = relationship(
        "Permission",
        back_populates="storeStaffMappings",
    )

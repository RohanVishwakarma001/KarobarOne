# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for user.
Defines the database schema, table columns, constraints, and relationships for user.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


# --------------------------------------------------------------------------------
# User Model
# Core identity table representing the global user base (auth + profile basics).
# Uses 'BaseModelWithUpdate' to automatically include 'createdAt' and 'updatedAt'.
# Python attribute names are camelCase; DB column names stay snake_case via
# the explicit 'name=' argument on mapped_column.
# --------------------------------------------------------------------------------
class User(BaseModelWithUpdate):
    __tablename__ = "users"

    # firstName: Given name of the user
    firstName: Mapped[str] = mapped_column(
        "first_name",
        String(100),
        nullable=False,
    )

    # lastName: Family/surname of the user (optional)
    lastName: Mapped[str | None] = mapped_column(
        "last_name",
        String(100),
        nullable=True,
    )

    # email: Unique login/contact email address
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    # mobile: Unique E.164 formatted contact number
    mobile: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
    )

    # whatsappMobile: Optional alternate WhatsApp contact number
    whatsappMobile: Mapped[str | None] = mapped_column(
        "whatsapp_mobile",
        String(15),
        nullable=True,
    )

    # passwordHash: bcrypt/argon2 hashed password
    passwordHash: Mapped[str] = mapped_column(
        "password_hash",
        String(255),
        nullable=False,
    )

    # isActive: Toggle to enable/disable login access
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    # isEmailVerified: True once the email has been confirmed
    isEmailVerified: Mapped[bool] = mapped_column(
        "is_email_verified",
        Boolean,
        default=False,
        nullable=False,
    )

    # isMobileVerified: True once the mobile number has been confirmed
    isMobileVerified: Mapped[bool] = mapped_column(
        "is_mobile_verified",
        Boolean,
        default=False,
        nullable=False,
    )

    # lastLoginAt: Timestamp of the most recent successful login
    lastLoginAt: Mapped[datetime | None] = mapped_column(
        "last_login_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # deletedAt: Soft delete marker; NULL means the record is active
    deletedAt: Mapped[datetime | None] = mapped_column(
        "deleted_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # roleMappings: Roles assigned to this user (global and/or tenant-scoped)
    roleMappings = relationship(
        "UserRoleMapping",
        back_populates="user",
        foreign_keys="UserRoleMapping.userId",
        cascade="all, delete-orphan",
    )

    # storePermissions: Store-level fine-grained permission overrides for this user
    storePermissions = relationship(
        "StoreStaffPermission",
        back_populates="user",
        foreign_keys="StoreStaffPermission.userId",
        cascade="all, delete-orphan",
    )

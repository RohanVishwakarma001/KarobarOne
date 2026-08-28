# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for userSecuritySetting.
Defines the database schema, table columns, constraints, and relationships for userSecuritySetting.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


# --------------------------------------------------------------------------------
# UserSecuritySetting Model
# Per-user security configuration: 2FA, lockout tracking, password change audit.
# Uses 'BaseModelWithUpdate' to automatically include 'createdAt' and 'updatedAt'.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class UserSecuritySetting(BaseModelWithUpdate):
    __tablename__ = "user_security_settings"

    # userId: The user this security configuration belongs to (one-to-one).
    userId: Mapped[uuid.UUID] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    # twoFactorEnabled: True if the user has enabled two-factor authentication.
    twoFactorEnabled: Mapped[bool] = mapped_column(
        "two_factor_enabled",
        Boolean,
        default=False,
        nullable=False,
    )

    # failedLoginCount: Consecutive failed login attempts since the last success.
    failedLoginCount: Mapped[int] = mapped_column(
        "failed_login_count",
        SmallInteger,
        default=0,
        nullable=False,
    )

    # accountLockedUntil: Timestamp until which the account is locked out (NULL if not locked).
    accountLockedUntil: Mapped[datetime | None] = mapped_column(
        "account_locked_until",
        DateTime(timezone=True),
        nullable=True,
    )

    # passwordChangedAt: Timestamp of the most recent password change.
    passwordChangedAt: Mapped[datetime | None] = mapped_column(
        "password_changed_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # user: One-to-one relationship back to the related User record.
    user = relationship("User")

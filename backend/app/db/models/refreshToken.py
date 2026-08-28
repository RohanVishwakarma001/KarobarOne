# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for refreshToken.
Defines the database schema, table columns, constraints, and relationships for refreshToken.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# RefreshToken Model
# Secure storage of JWT refresh tokens issued per device/session.
# Uses 'BaseUUID' since the audit timestamp here is 'createdAt' via server_default,
# matching the table schema's plain 'createdAt' column (no updatedAt needed).
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class RefreshToken(BaseUUID):
    __tablename__ = "refresh_tokens"

    # userId: The user this refresh token was issued to.
    # ondelete="CASCADE" removes tokens automatically when the user is deleted.
    userId: Mapped[uuid.UUID] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # tokenHash: Hashed representation of the refresh token (never store raw tokens).
    tokenHash: Mapped[str] = mapped_column(
        "token_hash",
        String(255),
        nullable=False,
    )

    # deviceName: Human-readable device label (e.g. 'Mousam's iPhone 14').
    deviceName: Mapped[str | None] = mapped_column(
        "device_name",
        String(100),
        nullable=True,
    )

    # deviceType: Device category (e.g. 'MOBILE', 'WEB', 'DESKTOP').
    deviceType: Mapped[str | None] = mapped_column(
        "device_type",
        String(50),
        nullable=True,
    )

    # ipAddress: IPv4/IPv6 address the token was issued from.
    ipAddress: Mapped[str | None] = mapped_column(
        "ip_address",
        String(45),
        nullable=True,
    )

    # expiresAt: Expiration timestamp after which the token is no longer valid.
    expiresAt: Mapped[datetime] = mapped_column(
        "expires_at",
        DateTime(timezone=True),
        nullable=False,
    )

    # revokedAt: Timestamp when the token was manually invalidated (e.g. logout).
    revokedAt: Mapped[datetime | None] = mapped_column(
        "revoked_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # createdAt: Timestamp when this refresh token was issued.
    createdAt: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # user: Relationship back to the related User record.
    user = relationship("User")

    # session: One-to-one back-reference to the active UserSession tied to this token.
    session = relationship(
        "UserSession",
        back_populates="refreshToken",
        uselist=False,
        cascade="all, delete-orphan",
    )

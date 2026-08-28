# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for userSession.
Defines the database schema, table columns, constraints, and relationships for userSession.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# UserSession Model
# Tracks active login sessions tied 1-to-1 with an issued refresh token.
# Uses 'BaseUUID' since timestamps here are explicit business fields
# (loginAt/logoutAt), not the generic 'createdAt' convention.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class UserSession(BaseUUID):
    __tablename__ = "user_sessions"

    # userId: The user this session belongs to.
    # ondelete="CASCADE" removes sessions automatically when the user is deleted.
    userId: Mapped[uuid.UUID] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # refreshTokenId: The refresh token issued for this session.
    # ondelete="CASCADE" removes the session automatically when the token is deleted.
    refreshTokenId: Mapped[uuid.UUID] = mapped_column(
        "refresh_token_id",
        UUID(as_uuid=True),
        ForeignKey(
            "refresh_tokens.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # loginAt: Timestamp marking the start of this session.
    loginAt: Mapped[datetime] = mapped_column(
        "login_at",
        DateTime(timezone=True),
        nullable=False,
    )

    # logoutAt: Timestamp marking when the session ended (NULL if still active).
    logoutAt: Mapped[datetime | None] = mapped_column(
        "logout_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # ipAddress: IPv4/IPv6 address the session originated from.
    ipAddress: Mapped[str | None] = mapped_column(
        "ip_address",
        String(45),
        nullable=True,
    )

    # userAgent: Raw User-Agent header string from the client.
    userAgent: Mapped[str | None] = mapped_column(
        "user_agent",
        Text,
        nullable=True,
    )

    # isActive: True while the session has not been logged out/revoked.
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    # user: Relationship back to the related User record.
    user = relationship("User")

    # refreshToken: Relationship back to the related RefreshToken record.
    refreshToken = relationship(
        "RefreshToken",
        back_populates="session",
    )

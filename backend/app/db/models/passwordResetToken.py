# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for passwordResetToken.
Defines the database schema, table columns, constraints, and relationships for passwordResetToken.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# PasswordResetToken Model
# Powers the forgot-password / password recovery flow.
# Uses 'BaseUUID' with an explicit 'createdAt' column matching the table schema.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class PasswordResetToken(BaseUUID):
    __tablename__ = "password_reset_tokens"

    # userId: The user requesting the password reset.
    # ondelete="CASCADE" removes reset tokens automatically when the user is deleted.
    userId: Mapped[uuid.UUID] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # tokenHash: Hashed representation of the reset token (never store raw tokens).
    tokenHash: Mapped[str] = mapped_column(
        "token_hash",
        String(255),
        nullable=False,
    )

    # expiresAt: Expiration timestamp after which the token is no longer valid.
    expiresAt: Mapped[datetime] = mapped_column(
        "expires_at",
        DateTime(timezone=True),
        nullable=False,
    )

    # usedAt: Timestamp when the token was consumed to complete a reset (NULL if unused).
    usedAt: Mapped[datetime | None] = mapped_column(
        "used_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # createdAt: Timestamp when the reset token was issued.
    createdAt: Mapped[datetime] = mapped_column(
        "createdAt",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # user: Relationship back to the related User record.
    user = relationship("User")

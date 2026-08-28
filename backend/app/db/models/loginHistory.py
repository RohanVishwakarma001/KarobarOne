# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for loginHistory.
Defines the database schema, table columns, constraints, and relationships for loginHistory.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# LoginHistory Model
# Immutable audit log of authentication attempts (successful and failed).
# Uses 'BaseUUID' with an explicit 'createdAt' column matching the table schema.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class LoginHistory(BaseUUID):
    __tablename__ = "login_history"

    # check_login_status: Restricts loginStatus to a fixed set of audit outcomes.
    __table_args__ = (
        CheckConstraint(
            "login_status IN ('SUCCESS', 'FAILED')",
            name="ck_login_status",
        ),
    )

    # userId: The user the attempt is attributed to (NULL if the email didn't match any user).
    userId: Mapped[uuid.UUID | None] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # email: Email address used in the login attempt (captured regardless of match success).
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ipAddress: IPv4/IPv6 address the attempt originated from.
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

    # loginStatus: Outcome of the attempt, either 'SUCCESS' or 'FAILED'.
    loginStatus: Mapped[str] = mapped_column(
        "login_status",
        String(20),
        nullable=False,
    )

    # failureReason: Optional explanation when loginStatus is 'FAILED'.
    failureReason: Mapped[str | None] = mapped_column(
        "failure_reason",
        String(255),
        nullable=True,
    )

    # createdAt: Timestamp when this audit entry was recorded.
    createdAt: Mapped[datetime] = mapped_column(
        "createdAt",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # user: Relationship back to the related User record (nullable).
    user = relationship("User")

# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for otpVerification.
Defines the database schema, table columns, constraints, and relationships for otpVerification.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, SmallInteger, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# OtpVerification Model
# OTP-based verification for login, signup, password reset, and transaction flows.
# Uses 'BaseUUID' with an explicit 'createdAt' column matching the table schema.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class OtpVerification(BaseUUID):
    __tablename__ = "otpVerifications"

    # check_otp_purpose: Restricts purpose to a fixed set of OTP use-cases.
    # check_otp_attempts: Caps verification attempts at 5 to prevent brute-forcing.
    __table_args__ = (
        CheckConstraint(
            "purpose IN ('LOGIN', 'SIGNUP', 'RESET', 'TRANSACTION')",
            name="ck_otp_purpose",
        ),
        CheckConstraint(
            "attempts <= 5",
            name="ck_otp_attempts",
        ),
    )

    # userId: The user this OTP was generated for.
    # ondelete="CASCADE" removes OTP records automatically when the user is deleted.
    userId: Mapped[uuid.UUID] = mapped_column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # purpose: The flow this OTP is securing ('LOGIN', 'SIGNUP', 'RESET', 'TRANSACTION').
    purpose: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # otpHash: Hashed representation of the OTP code (never store raw OTPs).
    otpHash: Mapped[str] = mapped_column(
        "otp_hash",
        String(255),
        nullable=False,
    )

    # expiresAt: Expiration timestamp after which the OTP is no longer valid.
    expiresAt: Mapped[datetime] = mapped_column(
        "expires_at",
        DateTime(timezone=True),
        nullable=False,
    )

    # verifiedAt: Timestamp when the OTP was successfully verified (NULL if unverified).
    verifiedAt: Mapped[datetime | None] = mapped_column(
        "verified_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # attempts: Number of verification attempts made so far (capped at 5).
    attempts: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        nullable=False,
    )

    # createdAt: Timestamp when this OTP was generated.
    createdAt: Mapped[datetime] = mapped_column(
        "createdAt",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # user: Relationship back to the related User record.
    user = relationship("User")

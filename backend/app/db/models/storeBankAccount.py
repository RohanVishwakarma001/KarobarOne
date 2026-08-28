# Owner: mousamdas156@gmail.com
"""
================================================================================
STORE BANK ACCOUNT MODEL
================================================================================
Yeh file dukaano ke bank accounts aur payment settlement details ko manage karti hai.
This model maps to the 'store_bank_accounts' table, containing bank registration 
and verification records for payouts.

Why it is used:
- Keeps track of the payout bank accounts connected to a store.
- Enforces the business constraint that a store can only have one primary bank account 
  at any given time.
================================================================================
"""

import uuid
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


class StoreBankAccount(BaseModel):
    """
    ORM Model representing a bank account linked to a Store.
    Inherits from BaseModel, getting 'id' and 'createdAt'.
    """
    __tablename__ = "store_bank_accounts"

    # ── Database Constraints & Indexes ─────────────────────────────────
    __table_args__ = (
        # PARTIAL UNIQUE INDEX:
        # This constraint ensures that for a given store_id, there can only be ONE 
        # bank account record where is_primary is TRUE.
        # It allows multiple non-primary accounts (is_primary = FALSE) but restricts 
        # primary accounts to exactly one.
        Index(
            "uq_store_bank_accounts_primary",
            "store_id",
            unique=True,
            postgresql_where=text("is_primary = TRUE"),
        ),
        # Ensure that account type is either SAVINGS or CURRENT
        CheckConstraint(
            "account_type IN ('SAVINGS', 'CURRENT')",
            name="ck_bank_account_type",
        ),
        # Ensure validation status is restricted to PENDING, VERIFIED, or REJECTED
        CheckConstraint(
            "verification_status IN ('PENDING', 'VERIFIED', 'REJECTED')",
            name="ck_bank_verification_status",
        ),
    )

    # Foreign key referencing the associated Store
    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        ForeignKey("stores.id"),
        nullable=False,
    )

    # Name of the bank account holder (e.g. "John Doe")
    accountHolderName: Mapped[str] = mapped_column(
        "account_holder_name",
        String(150),
        nullable=False,
    )

    # Name of the banking institution (e.g., "State Bank of India")
    bankName: Mapped[str] = mapped_column(
        "bank_name",
        String(150),
        nullable=False,
    )

    # Branch office location name
    branchName: Mapped[str | None] = mapped_column(
        "branch_name",
        String(150),
        nullable=True,
    )

    # Masked version of the account number for security/display (e.g., "******5678")
    accountNumberMasked: Mapped[str] = mapped_column(
        "account_number_masked",
        String(20),
        nullable=False,
    )

    # Indian Financial System Code (IFSC) for routing wire transfers (11 characters)
    ifscCode: Mapped[str] = mapped_column(
        "ifsc_code",
        String(11),
        nullable=False,
    )

    # Savings or Current account type (validated by check constraint)
    accountType: Mapped[str] = mapped_column(
        "account_type",
        String(30),
        nullable=False,
    )

    # Verification status of the bank account details
    verificationStatus: Mapped[str] = mapped_column(
        "verification_status",
        String(20),
        default="PENDING",
        nullable=False,
    )

    # Boolean flag indicating whether this is the primary bank account for payouts
    isPrimary: Mapped[bool] = mapped_column(
        "is_primary",
        Boolean,
        default=False,
        nullable=False,
    )

    # ── Relationships ──────────────────────────────────────────────────
    # Link back to the parent Store model
    store = relationship("Store", back_populates="bankAccounts")

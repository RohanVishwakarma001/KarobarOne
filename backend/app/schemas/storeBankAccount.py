# Owner: mousamdas156@gmail.com
"""
================================================================================
STORE BANK ACCOUNT DATA SCHEMAS
================================================================================
Yeh file payout bank accounts ke data validations (Create, Update, Response) handle karti hai.
This module defines Pydantic validation schemas for the StoreBankAccount entity.

Why it is used:
- Enforces strict length bounds on critical fields like IFSC codes (exactly 11 chars).
================================================================================
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ── Create Request Schema ──────────────────────────────────────────
class StoreBankAccountCreate(BaseModel):
    """
    Schema for validating bank account registration inputs.
    """
    # Associated Store
    storeId: uuid.UUID
    
    # Account holder's display name
    accountHolderName: str = Field(..., max_length=150)
    
    # Name of the banking corporation
    bankName: str = Field(..., max_length=150)
    
    # Local branch office location name
    branchName: str | None = Field(None, max_length=150)
    
    # Masked account number sequence
    accountNumberMasked: str = Field(..., max_length=20)
    
    # Financial routing code (IFSC code)
    ifscCode: str = Field(..., max_length=11)
    
    # Savings or Current type indicator
    accountType: str = Field("SAVINGS", max_length=30)
    
    # Account details validation status
    verificationStatus: str = Field("PENDING", max_length=20)
    
    # Primary account flag toggle
    isPrimary: bool = False


# ── Update Request Schema ──────────────────────────────────────────
class StoreBankAccountUpdate(BaseModel):
    """
    Schema for validating partial updates of store bank account settings.
    """
    accountHolderName: str | None = Field(None, max_length=150)
    bankName: str | None = Field(None, max_length=150)
    branchName: str | None = Field(None, max_length=150)
    accountNumberMasked: str | None = Field(None, max_length=20)
    ifscCode: str | None = Field(None, max_length=11)
    accountType: str | None = Field(None, max_length=30)
    verificationStatus: str | None = Field(None, max_length=20)
    isPrimary: bool | None = None


# ── Response Serialization Schema ────────────────────────────────────
class StoreBankAccountResponse(BaseModel):
    """
    Schema representing a bank account returned to the API client.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    storeId: uuid.UUID
    accountHolderName: str
    bankName: str
    branchName: str | None
    accountNumberMasked: str
    ifscCode: str
    accountType: str
    verificationStatus: str
    isPrimary: bool
    createdAt: datetime

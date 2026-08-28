# Owner: mousamdas156@gmail.com
"""
================================================================================
STORE BANK ACCOUNTS ENDPOINTS ROUTER
================================================================================
Yeh file bank accounts ke REST API endpoints expose karti hai.
This module defines the routing layer for managing payout bank accounts of stores.

Why it is used:
- Receives bank account additions and updates from merchants.
================================================================================
"""

import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.storeBankAccount import (
    StoreBankAccountCreate,
    StoreBankAccountResponse,
    StoreBankAccountUpdate,
)
from app.services.storeBankAccountService import StoreBankAccountService

# Router configuration
router = APIRouter(prefix="/store-bank-accounts", tags=["Store Bank Accounts"])


@router.post("/", response_model=StoreBankAccountResponse, status_code=status.HTTP_201_CREATED)
async def createBankAccount(
    data: StoreBankAccountCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Registers a new bank account. Returns 201 Created.
    """
    service = StoreBankAccountService(session)
    return await service.createBankAccount(data)


@router.get("/{bankAccountId}", response_model=StoreBankAccountResponse)
async def getBankAccount(
    bankAccountId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Fetches bank account details by database ID.
    """
    service = StoreBankAccountService(session)
    return await service.getBankAccount(bankAccountId)


@router.get("/", response_model=list[StoreBankAccountResponse])
async def listBankAccounts(
    storeId: uuid.UUID | None = Query(None),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists bank accounts, with optional filtering by storeId.
    """
    service = StoreBankAccountService(session)
    return await service.listBankAccounts(storeId=storeId)


@router.patch("/{bankAccountId}", response_model=StoreBankAccountResponse)
async def updateBankAccount(
    bankAccountId: uuid.UUID,
    data: StoreBankAccountUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates bank account details (such as toggling primary payout account status).
    """
    service = StoreBankAccountService(session)
    return await service.updateBankAccount(bankAccountId, data)


@router.delete("/{bankAccountId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteBankAccount(
    bankAccountId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Removes a bank account record. Returns 204 No Content.
    """
    service = StoreBankAccountService(session)
    await service.deleteBankAccount(bankAccountId)

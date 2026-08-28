# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/storeBankAccountService.py — Store Bank Account Service
# ================================================================================
# Why this file is used:
#   - Manages bank details validation and limits payout accounts.
#
# What components are inside:
#   - StoreBankAccountService:
#       - createBankAccount()  -> Registers bank info, verifying that only one
#                                 primary account exists.
#       - getBankAccount()     -> Resolves bank accounts.
#       - listBankAccounts()   -> Returns bank account entries.
#       - updateBankAccount()  -> Modifies bank parameters.
#       - deleteBankAccount()  -> Removes bank accounts.
# ================================================================================
"""
================================================================================
STORE BANK ACCOUNT SERVICE
================================================================================
Yeh file bank accounts ke registration aur primary accounts toggle ke business rules handle karti hai.
This service layer module implements settlement bank account management rules.

Why it is used:
- Coordinates the crucial business rule that a store can only have one primary bank account.
- Automatically toggles any previously primary account to non-primary if a new one is set.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.storeBankAccount import StoreBankAccount
from app.repositories.storeBankAccountRepository import StoreBankAccountRepository
from app.schemas.storeBankAccount import StoreBankAccountCreate, StoreBankAccountUpdate


class StoreBankAccountService:
    """
    Service class containing business rules for managing Store Bank Accounts.
    """

    def __init__(self, session: AsyncSession):
        self.repo = StoreBankAccountRepository(session)
        self.session = session

    async def createBankAccount(self, data: StoreBankAccountCreate) -> StoreBankAccount:
        """
        Registers a new bank account. If the new account is marked as the primary payout destination (isPrimary=True), 
        any existing primary bank account for the store is automatically updated to isPrimary=False.
        """
        if data.isPrimary:
            # Check if there is already an existing primary bank account for this store
            existingPrimary = await self.repo.getPrimary(data.storeId)
            if existingPrimary:
                # Toggle the old primary account to False to keep constraints valid
                await self.repo.update(existingPrimary, {"isPrimary": False})

        # Save and return the new bank account
        bankAccount = StoreBankAccount(**data.model_dump())
        result = await self.repo.create(bankAccount)
        await self.session.commit()
        return result

    async def getBankAccount(self, bankAccountId: uuid.UUID) -> StoreBankAccount:
        """
        Retrieves bank account information by its ID.
        """
        account = await self.repo.getById(bankAccountId)
        if not account:
            raise NotFoundError("StoreBankAccount", str(bankAccountId))
        return account

    async def listBankAccounts(self, storeId: uuid.UUID | None = None) -> Sequence[StoreBankAccount]:
        """
        Lists all registered bank accounts, with optional filtering by storeId.
        """
        return await self.repo.getAll(storeId=storeId)

    async def updateBankAccount(self, bankAccountId: uuid.UUID, data: StoreBankAccountUpdate) -> StoreBankAccount:
        """
        Updates an existing bank account. If it is being updated to primary (isPrimary=True), 
        any other primary bank account for the store is toggled to non-primary.
        """
        account = await self.repo.getById(bankAccountId)
        if not account:
            raise NotFoundError("StoreBankAccount", str(bankAccountId))

        updateData = data.model_dump(exclude_unset=True)
        # If the update payload sets this account as primary, find the old primary account and disable it.
        if updateData.get("isPrimary") is True:
            existingPrimary = await self.repo.getPrimary(account.storeId)
            # Make sure we don't deactivate the current account if it was already primary.
            if existingPrimary and existingPrimary.id != bankAccountId:
                await self.repo.update(existingPrimary, {"isPrimary": False})

        result = await self.repo.update(account, updateData)
        await self.session.commit()
        return result

    async def deleteBankAccount(self, bankAccountId: uuid.UUID) -> None:
        """
        Deletes a bank account record.
        """
        account = await self.repo.getById(bankAccountId)
        if not account:
            raise NotFoundError("StoreBankAccount", str(bankAccountId))
        await self.repo.delete(account)
        await self.session.commit()
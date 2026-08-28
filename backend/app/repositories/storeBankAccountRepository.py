# Owner: mousamdas156@gmail.com
"""
================================================================================
STORE BANK ACCOUNT DATABASE REPOSITORY
================================================================================
Yeh file store_bank_accounts table ke database transactions handle karti hai.
This repository class manages queries and writes for bank payout accounts.

Why it is used:
- Separates database operations from business-specific primary account toggle rules.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.storeBankAccount import StoreBankAccount


class StoreBankAccountRepository:
    """
    Handles CRUD operations and custom database queries for StoreBankAccount models.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getById(self, bankAccountId: uuid.UUID) -> StoreBankAccount | None:
        """
        Retrieves a StoreBankAccount by its unique primary key ID.
        """
        result = await self.session.execute(
            select(StoreBankAccount).where(StoreBankAccount.id == bankAccountId)
        )
        return result.scalar_one_or_none()

    async def getAll(self, storeId: uuid.UUID | None = None) -> Sequence[StoreBankAccount]:
        """
        Fetches all bank accounts sorted by creation date descending.
        If 'storeId' is provided, returns accounts belonging only to that store.
        """
        stmt = select(StoreBankAccount).order_by(StoreBankAccount.createdAt.desc())
        if storeId:
            stmt = stmt.where(StoreBankAccount.storeId == storeId)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def getPrimary(self, storeId: uuid.UUID) -> StoreBankAccount | None:
        """
        Finds the single Primary bank account currently active for a store.
        
        Why it is used:
        - Used by the bank services to find and unset the old primary account when a new one is set.
        """
        result = await self.session.execute(
            select(StoreBankAccount).where(
                StoreBankAccount.storeId == storeId,
                StoreBankAccount.isPrimary == True
            )
        )
        return result.scalar_one_or_none()

    async def create(self, bankAccount: StoreBankAccount) -> StoreBankAccount:
        """
        Registers a new StoreBankAccount in the database.
        """
        self.session.add(bankAccount)
        await self.session.flush()
        await self.session.refresh(bankAccount)
        return bankAccount

    async def update(self, bankAccount: StoreBankAccount, data: dict) -> StoreBankAccount:
        """
        Updates the values of an existing StoreBankAccount.
        """
        for key, value in data.items():
            setattr(bankAccount, key, value)
        await self.session.flush()
        await self.session.refresh(bankAccount)
        return bankAccount

    async def delete(self, bankAccount: StoreBankAccount) -> None:
        """
        Deletes a bank account record from the database.
        """
        await self.session.delete(bankAccount)
        await self.session.flush()

# Owner: mousamdas156@gmail.com
"""
================================================================================
STORE DATABASE REPOSITORY
================================================================================
Yeh file stores table ke liye database connectivity aur CRUD operations handle karti hai.
This repository class manages queries and transactions for the main Store entity.

Why it is used:
- Provides clean queries to find stores by ID or slug and separate DB access from router logic.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.store import Store


class StoreRepository:
    """
    Manages database access, queries, inserts, and deletions for the Store model.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getById(self, storeId: uuid.UUID) -> Store | None:
        """
        Retrieves a Store record by its unique primary key ID.
        """
        result = await self.session.execute(
            select(Store).where(Store.id == storeId)
        )
        return result.scalar_one_or_none()

    async def getBySlug(self, storeSlug: str) -> Store | None:
        """
        Retrieves a Store using its unique URL slug (e.g. 'johns-bakery').

        Why it is used:
        - Used to serve storefront information to customers browsing by the store's web slug.
        """
        result = await self.session.execute(
            select(Store).where(Store.storeSlug == storeSlug)
        )
        return result.scalar_one_or_none()

    async def getAll(self, tenantId: uuid.UUID | None = None) -> Sequence[Store]:
        """
        Fetches all stores sorted by creation date descending.
        If 'tenantId' is specified, returns only the stores owned by that merchant/tenant.
        """
        stmt = select(Store).order_by(Store.createdAt.desc())
        if tenantId:
            stmt = stmt.where(Store.tenantId == tenantId)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, store: Store) -> Store:
        """
        Registers a new Store in the database and flushes changes immediately.
        """
        self.session.add(store)
        await self.session.flush()
        await self.session.refresh(store)
        return store

    async def update(self, store: Store, data: dict) -> Store:
        """
        Performs a partial fields update of an existing Store record.
        """
        for key, value in data.items():
            setattr(store, key, value)
        await self.session.flush()
        await self.session.refresh(store)
        return store

    async def delete(self, store: Store) -> None:
        """
        Deletes a Store from the database, automatically cascade-deleting associated sections and bank accounts.
        """
        await self.session.delete(store)
        await self.session.flush()

    async def submitForApproval(self, store: Store) -> Store:
        """
        Marks a store as pending for admin approval.
        """
        store.approvalStatus = "PENDING"
        await self.session.flush()
        await self.session.refresh(store)
        return store

    async def publish(self, store: Store) -> Store:
        """
        Publishes an approved store.
        """
        store.isActive = True
        await self.session.flush()
        await self.session.refresh(store)
        return store
    async def updateTheme(self, store: Store, themeId: uuid.UUID) -> Store:
        """
        Updates the website theme for a store.
        """
        store.themeId = themeId
        await self.session.flush()
        await self.session.refresh(store)
        return store

# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: repositories/base.py — Generic Base Repository (Common CRUD Operations)
# ================================================================================
# Why this file is used:
#   - Provides reusable generic data-access utilities inherited by specific domain repositories.
#
# What components are inside:
#   - BaseRepository:
#       - getById()  -> Resolves records via primary keys.
#       - getAll()   -> Runs paginated queries with optional SQL where expressions.
#       - create()   -> Persists entities (flushes database transaction changes).
#       - update()   -> Merges modifications dynamically before committing.
#       - delete()   -> Schedules entities for transaction removal.
# ================================================================================
"""
Generic base repository with common CRUD operations.
Encapsulates basic SQLAlchemy querying logic to keep child repositories DRY.
"""

import uuid
from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

# T is bound to SQL Alchemy Declarative base models (Base)
T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Base class providing reusable async CRUD methods.
    Accepts a target model class and active database AsyncSession.
    """

    def __init__(self, model: type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def getById(self, recordId: uuid.UUID) -> T | None:
        """
        Fetches a record by its UUID primary key.
        """
        return await self.session.get(self.model, recordId)

    async def getAll(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: list[Any] | None = None,
    ) -> tuple[Sequence[T], int]:
        """
        Fetches records with server-side pagination (limit & offset).
        Executes a separate query to return the total matching count.
        """
        stmt = select(self.model)
        countStmt = select(func.count()).select_from(self.model)

        # Apply list of SQLAlchemy where-clauses if provided
        if filters:
            for f in filters:
                stmt = stmt.where(f)
                countStmt = countStmt.where(f)

        # Execute total count query
        total = (await self.session.execute(countStmt)).scalar() or 0
        
        # Execute paginated query
        itemsResult = await self.session.execute(
            stmt.offset(skip).limit(limit)
        )
        items = itemsResult.scalars().all()
        return items, total

    async def create(self, obj: T) -> T:
        """
        Adds a new object to the database context session.
        Uses flush() to trigger database-level defaults (like UUID/timestamps)
        and updates the object ID without committing the active transaction.
        """
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: T, data: dict[str, Any]) -> T:
        """
        Performs a dynamic partial update on an active model object.
        Iterates over fields to apply modifications before flushing.
        """
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        """
        Marks an object for deletion in the active session context.
        """
        await self.session.delete(obj)
        await self.session.flush()

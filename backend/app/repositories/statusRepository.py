# Owner: mousamdas156@gmail.com
"""
Repository for TenantStatus operations.
Tracks lookup tables containing various billing statuses.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tenantStatus import TenantStatus


class StatusRepository:
    """
    Manages lookups and writes for tenant subscription status presets.
    Does not inherit BaseRepository as PK is auto-incrementing integer instead of UUID.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def getAll(self) -> list[TenantStatus]:
        """
        Lists all billing statuses registered, sorted by ID index.
        """
        result = await self.session.execute(
            select(TenantStatus).order_by(TenantStatus.id)
        )
        return list(result.scalars().all())

    async def getById(self, statusId: int) -> TenantStatus | None:
        """
        Fetches a status preset by its integer ID.
        """
        return await self.session.get(TenantStatus, statusId)

    async def getByName(self, name: str) -> TenantStatus | None:
        """
        Looks up status mapping by name (e.g. 'ACTIVE', 'SUSPENDED').
        """
        result = await self.session.execute(
            select(TenantStatus).where(TenantStatus.statusName == name)
        )
        return result.scalar_one_or_none()

    async def create(self, status: TenantStatus) -> TenantStatus:
        """
        Creates a new billing status preset configuration in the lookup index.
        """
        self.session.add(status)
        await self.session.flush()
        await self.session.refresh(status)
        return status


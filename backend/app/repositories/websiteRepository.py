import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.website import Website


class WebsiteRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, website: Website) -> Website:
        self.session.add(website)
        await self.session.flush()
        await self.session.refresh(website)
        return website

    async def getById(self, websiteId: uuid.UUID) -> Website | None:
        result = await self.session.execute(
            select(Website).where(Website.id == websiteId)
        )
        return result.scalar_one_or_none()

    async def getBySlug(self, slug: str) -> Website | None:
        result = await self.session.execute(
            select(Website).where(Website.slug == slug)
        )
        return result.scalar_one_or_none()

    async def getByTenant(self, tenantId: uuid.UUID) -> Website | None:
        result = await self.session.execute(
            select(Website).where(Website.tenantId == tenantId)
        )
        return result.scalar_one_or_none()

    async def getByStatus(self, status: str) -> list[Website]:
        result = await self.session.execute(
            select(Website)
            .where(Website.status == status)
            .order_by(Website.createdAt.desc())
        )
        return list(result.scalars().all())

    async def update(self, website: Website, data: dict) -> Website:
        for key, value in data.items():
            setattr(website, key, value)

        await self.session.flush()
        await self.session.refresh(website)
        return website

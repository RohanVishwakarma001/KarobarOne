import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.websiteMedia import WebsiteMedia


class WebsiteMediaRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getByWebsiteId(
        self,
        websiteId: uuid.UUID,
    ) -> WebsiteMedia | None:
        result = await self.session.execute(
            select(WebsiteMedia).where(
                WebsiteMedia.websiteId == websiteId
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        media: WebsiteMedia,
    ) -> WebsiteMedia:
        self.session.add(media)
        await self.session.flush()
        await self.session.refresh(media)
        return media

    async def update(
        self,
        media: WebsiteMedia,
        data: dict,
    ) -> WebsiteMedia:
        for key, value in data.items():
            setattr(media, key, value)

        await self.session.flush()
        await self.session.refresh(media)

        return media

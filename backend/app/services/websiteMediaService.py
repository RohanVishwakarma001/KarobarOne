import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.websiteMedia import WebsiteMedia
from app.db.models.website import Website
from app.repositories.websiteMediaRepository import WebsiteMediaRepository


class WebsiteMediaService:

    def __init__(self, session: AsyncSession):
        self.repo = WebsiteMediaRepository(session)
        self.session = session

    async def ensureWebsite(
        self,
        websiteId: uuid.UUID,
    ) -> Website:
        from sqlalchemy import select

        result = await self.session.execute(
            select(Website).where(
                Website.id == websiteId
            )
        )

        website = result.scalar_one_or_none()

        if not website:
            raise NotFoundError(
                "Website",
                str(websiteId),
            )

        return website

    async def createMedia(
        self,
        websiteId: uuid.UUID,
        logo: str | None,
        banner: str | None,
        gallery: list[str] | None,
    ) -> WebsiteMedia:

        await self.ensureWebsite(websiteId)

        existing = await self.repo.getByWebsiteId(
            websiteId
        )

        if existing:
            raise ConflictError(
                f"Website media already exists for website "
                f"'{websiteId}'"
            )

        media = WebsiteMedia(
            websiteId=websiteId,
            logo=logo,
            banner=banner,
            gallery=gallery,
        )

        result = await self.repo.create(media)

        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def getMedia(
        self,
        websiteId: uuid.UUID,
    ) -> WebsiteMedia:

        await self.ensureWebsite(websiteId)

        media = await self.repo.getByWebsiteId(
            websiteId
        )

        if not media:
            raise NotFoundError(
                "WebsiteMedia",
                str(websiteId),
            )

        return media

    async def updateMedia(
        self,
        websiteId: uuid.UUID,
        data: dict,
    ) -> WebsiteMedia:

        await self.ensureWebsite(websiteId)

        media = await self.repo.getByWebsiteId(
            websiteId
        )

        if not media:
            raise NotFoundError(
                "WebsiteMedia",
                str(websiteId),
            )

        result = await self.repo.update(
            media,
            data,
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

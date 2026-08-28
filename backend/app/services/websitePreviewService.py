import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.website import Website
from app.db.models.websiteMedia import WebsiteMedia
from app.db.models.websiteSection import WebsiteSection
from app.db.models.websiteTheme import WebsiteTheme


class WebsitePreviewService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getPreviewBySlug(
        self,
        slug: str,
    ) -> dict:

        result = await self.session.execute(
            select(Website).where(
                Website.slug == slug
            )
        )

        website = result.scalar_one_or_none()

        if not website:
            raise NotFoundError(
                "Website",
                slug,
            )

        sectionsResult = await self.session.execute(
            select(WebsiteSection)
            .where(
                WebsiteSection.websiteId == website.id
            )
            .order_by(
                WebsiteSection.createdAt.asc()
            )
        )

        sections = list(
            sectionsResult.scalars().all()
        )

        mediaResult = await self.session.execute(
            select(WebsiteMedia)
            .where(
                WebsiteMedia.websiteId == website.id
            )
        )

        media = mediaResult.scalar_one_or_none()

        theme = None

        if website.theme:
            themeResult = await self.session.execute(
                select(WebsiteTheme)
                .where(
                    (
                        WebsiteTheme.themeCode
                        == website.theme
                    )
                    |
                    (
                        WebsiteTheme.themeName
                        == website.theme
                    )
                )
                .where(
                    WebsiteTheme.isActive.is_(True)
                )
            )

            theme = themeResult.scalar_one_or_none()

        websiteData = {
            "id": website.id,
            "tenantId": website.tenantId,
            "companyName": website.companyName,
            "slug": website.slug,
            "businessType": website.businessType,
            "theme": website.theme,
            "status": website.status,
            "plan": website.plan,
            "domain": website.domain,
            "createdAt": website.createdAt,
        }

        return {
            "website": websiteData,
            "sections": sections,
            "media": media,
            "theme": theme,
            "preview": True,
        }

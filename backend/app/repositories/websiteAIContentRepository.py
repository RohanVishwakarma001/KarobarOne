import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.websiteAIContent import WebsiteAIContent


class WebsiteAIContentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getById(
        self,
        contentId: uuid.UUID,
    ) -> WebsiteAIContent | None:
        result = await self.session.execute(
            select(WebsiteAIContent).where(
                WebsiteAIContent.id == contentId
            )
        )
        return result.scalar_one_or_none()

    async def getByStoreId(
        self,
        storeId: uuid.UUID,
    ) -> Sequence[WebsiteAIContent]:
        result = await self.session.execute(
            select(WebsiteAIContent)
            .where(WebsiteAIContent.storeId == storeId)
            .order_by(WebsiteAIContent.createdAt.desc())
        )
        return result.scalars().all()

    async def create(
        self,
        content: WebsiteAIContent,
    ) -> WebsiteAIContent:
        self.session.add(content)
        await self.session.flush()
        await self.session.refresh(content)
        return content

    async def update(
        self,
        content: WebsiteAIContent,
        data: dict,
    ) -> WebsiteAIContent:
        for key, value in data.items():
            setattr(content, key, value)

        await self.session.flush()
        await self.session.refresh(content)
        return content

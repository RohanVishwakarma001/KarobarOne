import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.websiteAIContent import WebsiteAIContent
from app.repositories.websiteAIContentRepository import (
    WebsiteAIContentRepository,
)
from app.schemas.websiteAIContent import (
    WebsiteAIContentCreate,
    WebsiteAIContentUpdate,
)


class WebsiteAIContentService:

    def __init__(self, session: AsyncSession):
        self.repo = WebsiteAIContentRepository(session)
        self.session = session

    async def getById(
        self,
        contentId: uuid.UUID,
    ) -> WebsiteAIContent:
        content = await self.repo.getById(contentId)

        if not content:
            raise NotFoundError(
                "Website AI content",
                str(contentId),
            )

        return content

    async def getByStoreId(
        self,
        storeId: uuid.UUID,
    ):
        return await self.repo.getByStoreId(storeId)

    async def create(
        self,
        data: WebsiteAIContentCreate,
    ) -> WebsiteAIContent:
        payload = data.model_dump()
        payload["contentMetadata"] = payload.pop("metadata", None)

        content = WebsiteAIContent(
            **payload,
            status="GENERATED",
        )

        result = await self.repo.create(content)
        await self.session.commit()

        return result

    async def update(
        self,
        contentId: uuid.UUID,
        data: WebsiteAIContentUpdate,
    ) -> WebsiteAIContent:
        content = await self.getById(contentId)

        updateData = data.model_dump(exclude_unset=True)

        if "metadata" in updateData:
            updateData["contentMetadata"] = updateData.pop("metadata")

        result = await self.repo.update(
            content,
            updateData,
        )

        await self.session.commit()

        return result

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.websitePublishLog import WebsitePublishLog
from app.repositories.websitePublishLogRepository import (
    WebsitePublishLogRepository,
)
from app.schemas.websitePublishLog import WebsitePublishLogCreate


class WebsitePublishLogService:

    def __init__(self, session: AsyncSession):
        self.repo = WebsitePublishLogRepository(session)
        self.session = session

    async def getById(
        self,
        logId: uuid.UUID,
    ) -> WebsitePublishLog:
        log = await self.repo.getById(logId)

        if not log:
            raise NotFoundError(
                "Website publish log",
                str(logId),
            )

        return log

    async def getByStoreId(
        self,
        storeId: uuid.UUID,
    ):
        return await self.repo.getByStoreId(storeId)

    async def create(
        self,
        data: WebsitePublishLogCreate,
    ) -> WebsitePublishLog:
        log = WebsitePublishLog(
            **data.model_dump(),
            publishedAt=(
                datetime.now(timezone.utc)
                if data.status.upper() == "SUCCESS"
                else None
            ),
        )

        result = await self.repo.create(log)
        await self.session.commit()

        return result

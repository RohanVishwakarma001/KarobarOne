import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.websitePublishLog import WebsitePublishLog


class WebsitePublishLogRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getById(
        self,
        logId: uuid.UUID,
    ) -> WebsitePublishLog | None:
        result = await self.session.execute(
            select(WebsitePublishLog).where(
                WebsitePublishLog.id == logId
            )
        )
        return result.scalar_one_or_none()

    async def getByStoreId(
        self,
        storeId: uuid.UUID,
    ) -> Sequence[WebsitePublishLog]:
        result = await self.session.execute(
            select(WebsitePublishLog)
            .where(WebsitePublishLog.storeId == storeId)
            .order_by(WebsitePublishLog.createdAt.desc())
        )
        return result.scalars().all()

    async def create(
        self,
        log: WebsitePublishLog,
    ) -> WebsitePublishLog:
        self.session.add(log)
        await self.session.flush()
        await self.session.refresh(log)
        return log

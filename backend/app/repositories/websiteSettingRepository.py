import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.websiteSetting import WebsiteSetting


class WebsiteSettingRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getByStoreId(
        self,
        storeId: uuid.UUID,
    ) -> WebsiteSetting | None:
        result = await self.session.execute(
            select(WebsiteSetting).where(
                WebsiteSetting.storeId == storeId
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        setting: WebsiteSetting,
    ) -> WebsiteSetting:
        self.session.add(setting)
        await self.session.flush()
        await self.session.refresh(setting)
        return setting

    async def update(
        self,
        setting: WebsiteSetting,
        data: dict,
    ) -> WebsiteSetting:
        for key, value in data.items():
            setattr(setting, key, value)

        await self.session.flush()
        await self.session.refresh(setting)
        return setting

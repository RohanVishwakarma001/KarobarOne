import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.websiteSetting import WebsiteSetting
from app.repositories.websiteSettingRepository import WebsiteSettingRepository
from app.schemas.websiteSetting import (
    WebsiteSettingCreate,
    WebsiteSettingUpdate,
)


class WebsiteSettingService:

    def __init__(self, session: AsyncSession):
        self.repo = WebsiteSettingRepository(session)
        self.session = session

    async def getByStoreId(self, storeId: uuid.UUID) -> WebsiteSetting:
        setting = await self.repo.getByStoreId(storeId)

        if not setting:
            raise NotFoundError("Website settings", str(storeId))

        return setting

    async def create(
        self,
        data: WebsiteSettingCreate,
    ) -> WebsiteSetting:
        existing = await self.repo.getByStoreId(data.storeId)

        if existing:
            raise ConflictError(
                f"Website settings already exist for store '{data.storeId}'"
            )

        setting = WebsiteSetting(**data.model_dump())

        result = await self.repo.create(setting)
        await self.session.commit()

        return result

    async def update(
        self,
        storeId: uuid.UUID,
        data: WebsiteSettingUpdate,
    ) -> WebsiteSetting:
        setting = await self.repo.getByStoreId(storeId)

        if not setting:
            raise NotFoundError("Website settings", str(storeId))

        updateData = data.model_dump(exclude_unset=True)

        result = await self.repo.update(setting, updateData)
        await self.session.commit()

        return result

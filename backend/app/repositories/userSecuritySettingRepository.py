# Owner: mousamdas156@gmail.com
"""
Repository layer for UserSecuritySetting.
Handles direct database queries for per-user security configuration.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.userSecuritySetting import UserSecuritySetting


class UserSecuritySettingRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getByUserId(self, userId: uuid.UUID) -> UserSecuritySetting | None:
        """
        Handles the get by user id functionality.
        """
        result = await self.session.execute(
            select(UserSecuritySetting).where(
                UserSecuritySetting.userId == userId
            )
        )
        return result.scalar_one_or_none()

    async def create(self, setting: UserSecuritySetting) -> UserSecuritySetting:
        """
        Handles the create functionality.
        """
        self.session.add(setting)
        await self.session.flush()
        await self.session.refresh(setting)
        return setting

    async def update(self, setting: UserSecuritySetting, data: dict) -> UserSecuritySetting:
        """
        Handles the update functionality.
        """
        for key, value in data.items():
            setattr(setting, key, value)
        await self.session.flush()
        await self.session.refresh(setting)
        return setting

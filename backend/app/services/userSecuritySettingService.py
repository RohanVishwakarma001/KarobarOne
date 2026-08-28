# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/userSecuritySettingService.py — User Security Settings Service
# ================================================================================
# Why this file is used:
#   - Manages lockouts, credentials policies, and settings.
#
# What components are inside:
#   - MAX_FAILED_LOGIN_ATTEMPTS -> Lock thresholds.
#   - LOCKOUT_DURATION_MINUTES  -> Duration of lockouts in minutes.
#   - UserSecuritySettingService:
#       - getOrCreate()         -> Lazily builds setting records.
#       - updateSettings()      -> Modifies security variables.
#       - recordFailedLogin()   -> Increments failure counts, locking settings when needed.
#       - resetFailedLogin()    -> Clears lockout flags.
# ================================================================================
"""
Service layer for UserSecuritySetting.
Handles per-user security configuration: 2FA, lockouts, password-change audit.
"""

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.userSecuritySetting import UserSecuritySetting
from app.repositories.userRepository import UserRepository
from app.repositories.userSecuritySettingRepository import (
    UserSecuritySettingRepository,
)
from app.schemas.userSecuritySetting import UserSecuritySettingUpdate

MAX_FAILED_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


class UserSecuritySettingService:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = UserSecuritySettingRepository(session)
        self.userRepo = UserRepository(session)
        self.session = session

    async def getOrCreate(self, userId: uuid.UUID) -> UserSecuritySetting:
        """
        Retrieves the user's security settings, creating a default record
        on first access (lazy initialization).
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))

        setting = await self.repo.getByUserId(userId)
        if setting:
            return setting

        setting = UserSecuritySetting(userId=userId)
        result = await self.repo.create(setting)
        await self.session.commit()
        return result

    async def updateSettings(
        self,
        userId: uuid.UUID,
        data: UserSecuritySettingUpdate,
    ) -> UserSecuritySetting:
        """
        """
        setting = await self.getOrCreate(userId)
        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return setting
        result = await self.repo.update(setting, updateData)
        await self.session.commit()
        return result

    async def recordFailedLogin(self, userId: uuid.UUID) -> UserSecuritySetting:
        """
        Increments the failed login counter and locks the account once the
        threshold is exceeded.
        """
        setting = await self.getOrCreate(userId)
        newCount = setting.failedLoginCount + 1
        updateData: dict = {"failedLoginCount": newCount}
        if newCount >= MAX_FAILED_LOGIN_ATTEMPTS:
            updateData["accountLockedUntil"] = datetime.now(
                timezone.utc
            ) + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        result = await self.repo.update(setting, updateData)
        await self.session.commit()
        return result

    async def resetFailedLogin(self, userId: uuid.UUID) -> UserSecuritySetting:
        """
        Clears the failed login counter and lockout after a successful login.
        """
        setting = await self.getOrCreate(userId)
        result = await self.repo.update(
            setting,
            {"failedLoginCount": 0, "accountLockedUntil": None},
        )
        await self.session.commit()
        return result
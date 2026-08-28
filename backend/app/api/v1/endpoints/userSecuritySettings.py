# Owner: mousamdas156@gmail.com
"""
Router layer for UserSecuritySetting.
Exposes endpoints to view and update per-user security configuration.
"""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.userSecuritySetting import (
    UserSecuritySettingResponse,
    UserSecuritySettingUpdate,
)
from app.services.userSecuritySettingService import UserSecuritySettingService

router = APIRouter(prefix="/users/{userId}/security-settings", tags=["User Security Settings"])


@router.get("/", response_model=UserSecuritySettingResponse)
async def getSettings(
    userId: uuid.UUID,
    db: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserSecuritySettingService(db)
    return await service.getOrCreate(userId)


@router.patch("/", response_model=UserSecuritySettingResponse)
async def updateSettings(
    userId: uuid.UUID,
    data: UserSecuritySettingUpdate,
    db: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserSecuritySettingService(db)
    return await service.updateSettings(userId, data)

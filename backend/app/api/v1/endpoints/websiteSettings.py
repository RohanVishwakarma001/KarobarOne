import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.websiteSetting import (
    WebsiteSettingCreate,
    WebsiteSettingResponse,
    WebsiteSettingUpdate,
)
from app.services.websiteSettingService import WebsiteSettingService


router = APIRouter(
    prefix="/website-settings",
    tags=["Website Settings"],
)


@router.post(
    "/",
    response_model=WebsiteSettingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def createWebsiteSetting(
    data: WebsiteSettingCreate,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteSettingService(session)
    return await service.create(data)


@router.get(
    "/store/{storeId}",
    response_model=WebsiteSettingResponse,
)
async def getWebsiteSetting(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteSettingService(session)
    return await service.getByStoreId(storeId)


@router.patch(
    "/store/{storeId}",
    response_model=WebsiteSettingResponse,
)
async def updateWebsiteSetting(
    storeId: uuid.UUID,
    data: WebsiteSettingUpdate,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteSettingService(session)
    return await service.update(storeId, data)

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.websitePublishLog import (
    WebsitePublishLogCreate,
    WebsitePublishLogResponse,
)
from app.services.websitePublishLogService import WebsitePublishLogService


router = APIRouter(
    prefix="/website-publish-logs",
    tags=["Website Publish Logs"],
)


@router.post(
    "/",
    response_model=WebsitePublishLogResponse,
    status_code=status.HTTP_201_CREATED,
)
async def createWebsitePublishLog(
    data: WebsitePublishLogCreate,
    session: AsyncSession = Depends(getDb),
):
    service = WebsitePublishLogService(session)
    return await service.create(data)


@router.get(
    "/{logId}",
    response_model=WebsitePublishLogResponse,
)
async def getWebsitePublishLog(
    logId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = WebsitePublishLogService(session)
    return await service.getById(logId)


@router.get(
    "/store/{storeId}",
    response_model=list[WebsitePublishLogResponse],
)
async def listWebsitePublishLogs(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = WebsitePublishLogService(session)
    return await service.getByStoreId(storeId)

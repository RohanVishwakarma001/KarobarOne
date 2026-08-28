import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.websiteAIContent import (
    WebsiteAIContentCreate,
    WebsiteAIContentResponse,
    WebsiteAIContentUpdate,
)
from app.services.websiteAIContentService import WebsiteAIContentService


router = APIRouter(
    prefix="/website-ai-content",
    tags=["Website AI Content"],
)


@router.post(
    "/",
    response_model=WebsiteAIContentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def createWebsiteAIContent(
    data: WebsiteAIContentCreate,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteAIContentService(session)
    return await service.create(data)


@router.get(
    "/{contentId}",
    response_model=WebsiteAIContentResponse,
)
async def getWebsiteAIContent(
    contentId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteAIContentService(session)
    return await service.getById(contentId)


@router.get(
    "/store/{storeId}",
    response_model=list[WebsiteAIContentResponse],
)
async def listWebsiteAIContent(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteAIContentService(session)
    return await service.getByStoreId(storeId)


@router.patch(
    "/{contentId}",
    response_model=WebsiteAIContentResponse,
)
async def updateWebsiteAIContent(
    contentId: uuid.UUID,
    data: WebsiteAIContentUpdate,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteAIContentService(session)
    return await service.update(contentId, data)

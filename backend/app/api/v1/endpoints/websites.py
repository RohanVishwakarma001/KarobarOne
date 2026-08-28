import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.website import (
    WebsiteCreate,
    WebsiteResponse,
    WebsiteSubmitRequest,
    WebsiteUpdate,
)
from app.schemas.websitePreview import WebsitePreviewResponse
from app.services.websiteService import WebsiteService
from app.services.websitePreviewService import WebsitePreviewService
from app.core.exceptionsCompat import NotFoundError


router = APIRouter(
    prefix="/websites",
    tags=["Websites"],
)


@router.post(
    "/create",
    response_model=WebsiteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def createWebsite(
    data: WebsiteCreate,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).createWebsite(data)


@router.put(
    "/update",
    response_model=WebsiteResponse,
)
async def updateWebsite(
    websiteId: uuid.UUID,
    data: WebsiteUpdate,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).updateWebsite(
        websiteId,
        data,
    )


@router.get(
    "/{websiteId}",
    response_model=WebsiteResponse,
)
async def getWebsite(
    websiteId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).getWebsite(websiteId)


@router.post(
    "/submit",
    response_model=WebsiteResponse,
)
async def submitWebsite(
    data: WebsiteSubmitRequest,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).submitWebsite(
        data.websiteId
    )


@router.get(
    "/preview/{slug}",
    response_model=WebsitePreviewResponse,
)
async def previewWebsite(
    slug: str,
    session: AsyncSession = Depends(getDb),
):
    return await WebsitePreviewService(
        session
    ).getPreviewBySlug(slug)

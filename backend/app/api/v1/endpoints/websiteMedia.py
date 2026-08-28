import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.websiteMedia import (
    WebsiteMediaCreate,
    WebsiteMediaUpdate,
    WebsiteMediaResponse,
)
from app.services.websiteMediaService import WebsiteMediaService


router = APIRouter(
    prefix="/website-media",
    tags=["Website Media"],
)


@router.post(
    "/",
    response_model=WebsiteMediaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def createWebsiteMedia(
    data: WebsiteMediaCreate,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteMediaService(
        session
    ).createMedia(
        websiteId=data.websiteId,
        logo=data.logo,
        banner=data.banner,
        gallery=data.gallery,
    )


@router.get(
    "/website/{websiteId}",
    response_model=WebsiteMediaResponse,
)
async def getWebsiteMedia(
    websiteId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteMediaService(
        session
    ).getMedia(websiteId)


@router.patch(
    "/website/{websiteId}",
    response_model=WebsiteMediaResponse,
)
async def updateWebsiteMedia(
    websiteId: uuid.UUID,
    data: WebsiteMediaUpdate,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteMediaService(
        session
    ).updateMedia(
        websiteId,
        data.model_dump(exclude_unset=True),
    )

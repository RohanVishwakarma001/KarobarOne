import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.website import (
    WebsiteResponse,
    WebsiteStatusRequest,
)
from app.services.websiteService import WebsiteService


router = APIRouter(
    prefix="/admin/websites",
    tags=["Admin Websites"],
)


@router.get(
    "/pending",
    response_model=list[WebsiteResponse],
)
async def getPendingWebsites(
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).listPending()


@router.get(
    "/{websiteId}",
    response_model=WebsiteResponse,
)
async def getAdminWebsite(
    websiteId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).getWebsite(websiteId)


@router.post(
    "/approve",
    response_model=WebsiteResponse,
)
async def approveWebsite(
    data: WebsiteStatusRequest,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).approveWebsite(data.websiteId)


@router.post(
    "/reject",
    response_model=WebsiteResponse,
)
async def rejectWebsite(
    data: WebsiteStatusRequest,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).rejectWebsite(data.websiteId)


@router.post(
    "/publish",
    response_model=WebsiteResponse,
)
async def publishWebsite(
    data: WebsiteStatusRequest,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteService(
        session
    ).publishWebsite(data.websiteId)

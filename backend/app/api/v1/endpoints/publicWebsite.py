from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.website import WebsiteResponse
from app.services.websiteService import WebsiteService
from app.core.exceptionsCompat import NotFoundError

router = APIRouter(tags=["Public Website"])


@router.get(
    "/company/{slug}",
    response_model=WebsiteResponse,
)
async def getPublicWebsite(
    slug: str,
    session: AsyncSession = Depends(getDb),
):
    website = await WebsiteService(session).repo.getBySlug(slug)

    if not website:
        raise NotFoundError("Website", slug)

    if website.status != "LIVE":
        raise NotFoundError("Published Website", slug)

    return website


@router.get(
    "/",
    response_model=WebsiteResponse,
)
async def getWebsiteByDomain(
    host: str | None = Header(default=None),
    session: AsyncSession = Depends(getDb),
):
    if not host:
        raise NotFoundError("Website", "Host header missing")

    result = await WebsiteService(session).repo.session.execute(
        __import__("sqlalchemy").select(
            __import__("app.db.models.website", fromlist=["Website"]).Website
        ).where(
            __import__("app.db.models.website", fromlist=["Website"]).Website.domain == host
        )
    )

    website = result.scalar_one_or_none()

    if not website or website.status != "LIVE":
        raise NotFoundError("Published Website", host)

    return website

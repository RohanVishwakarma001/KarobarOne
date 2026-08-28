import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.domain import DomainRead
from app.services.domainVerificationService import (
    DomainVerificationService,
)


router = APIRouter(
    prefix="/domains",
    tags=["Domain Verification"],
)


@router.post(
    "/{domainId}/verification-token",
    response_model=DomainRead,
)
async def generateDomainVerificationToken(
    domainId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    return await DomainVerificationService(
        session
    ).generateVerificationToken(domainId)


@router.post(
    "/{domainId}/verify",
    response_model=DomainRead,
)
async def verifyDomainDns(
    domainId: uuid.UUID,
    verificationToken: str,
    session: AsyncSession = Depends(getDb),
):
    return await DomainVerificationService(
        session
    ).verifyDns(
        domainId,
        verificationToken,
    )

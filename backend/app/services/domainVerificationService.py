import secrets
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import (
    ConflictError,
    NotFoundError,
)
from app.db.models.tenantDomainMapping import TenantDomainMapping
from app.repositories.domainRepository import DomainRepository


class DomainVerificationService:

    def __init__(self, session: AsyncSession):
        self.repo = DomainRepository(session)
        self.session = session

    async def getDomain(
        self,
        domainId: uuid.UUID,
    ) -> TenantDomainMapping:

        domain = await self.repo.getById(domainId)

        if not domain:
            raise NotFoundError(
                "Domain",
                str(domainId),
            )

        return domain

    async def generateVerificationToken(
        self,
        domainId: uuid.UUID,
    ) -> TenantDomainMapping:

        domain = await self.getDomain(domainId)

        if not domain.customDomain:
            raise ConflictError(
                "DNS verification requires a custom domain"
            )

        domain.dnsVerificationToken = (
            secrets.token_urlsafe(32)
        )
        domain.dnsVerified = False

        await self.session.commit()
        await self.session.refresh(domain)

        return domain

    async def verifyDns(
        self,
        domainId: uuid.UUID,
        verificationToken: str,
    ) -> TenantDomainMapping:

        domain = await self.getDomain(domainId)

        if not domain.customDomain:
            raise ConflictError(
                "DNS verification requires a custom domain"
            )

        if not domain.dnsVerificationToken:
            raise ConflictError(
                "Generate a DNS verification token first"
            )

        if not secrets.compare_digest(
            domain.dnsVerificationToken,
            verificationToken,
        ):
            raise ConflictError(
                "Invalid DNS verification token"
            )

        domain.dnsVerified = True

        await self.session.commit()
        await self.session.refresh(domain)

        return domain

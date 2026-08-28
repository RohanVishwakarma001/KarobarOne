import re
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.website import Website
from app.repositories.websiteRepository import WebsiteRepository
from app.schemas.website import WebsiteCreate, WebsiteUpdate


class WebsiteService:

    def __init__(self, session: AsyncSession):
        self.repo = WebsiteRepository(session)
        self.session = session

    def generateSlug(self, companyName: str) -> str:
        slug = companyName.lower().strip()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")

        if not slug:
            raise ConflictError(
                "Company name cannot generate a valid slug"
            )

        return slug

    async def resolveTheme(
        self,
        businessType: str,
    ) -> str | None:
        """
        Resolves an active website theme for the business type.

        If no exact theme is found, the first active theme is used.
        """
        from app.db.models.websiteTheme import WebsiteTheme
        from sqlalchemy import select

        result = await self.session.execute(
            select(WebsiteTheme)
            .where(WebsiteTheme.isActive.is_(True))
            .order_by(WebsiteTheme.themeName.asc())
        )

        themes = list(result.scalars().all())

        if not themes:
            return None

        business = businessType.lower().strip()

        # Try matching the business type against theme code/name.
        for theme in themes:
            themeName = (theme.themeName or "").lower()
            themeCode = (theme.themeCode or "").lower()

            if (
                business in themeName
                or business in themeCode
                or themeName in business
                or themeCode in business
            ):
                return theme.themeCode

        # Safe fallback.
        return themes[0].themeCode

    async def getWebsite(
        self,
        websiteId: uuid.UUID,
    ) -> Website:
        website = await self.repo.getById(websiteId)

        if not website:
            raise NotFoundError(
                "Website",
                str(websiteId),
            )

        return website

    async def createWebsite(
        self,
        data: WebsiteCreate,
    ) -> Website:

        existing = await self.repo.getByTenant(
            data.tenantId
        )

        if existing:
            raise ConflictError(
                f"Website already exists for tenant "
                f"'{data.tenantId}'"
            )

        baseSlug = self.generateSlug(
            data.companyName
        )

        slug = baseSlug

        assignedTheme = data.theme

        if not assignedTheme:
            assignedTheme = await self.resolveTheme(
                data.businessType
            )

        existingSlug = await self.repo.getBySlug(
            slug
        )

        if existingSlug:
            slug = (
                f"{baseSlug}-"
                f"{str(uuid.uuid4())[:8]}"
            )

        website = Website(
            tenantId=data.tenantId,
            companyName=data.companyName,
            slug=slug,
            businessType=data.businessType,
            theme=assignedTheme,
            status="DRAFT",
            plan=data.plan,
            domain=data.domain,
        )

        result = await self.repo.create(
            website
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def updateWebsite(
        self,
        websiteId: uuid.UUID,
        data: WebsiteUpdate,
    ) -> Website:

        website = await self.getWebsite(
            websiteId
        )

        if website.status == "LIVE":
            raise ConflictError(
                "LIVE website cannot be edited directly"
            )

        updateData = data.model_dump(
            exclude_unset=True
        )

        if not updateData:
            return website

        if "companyName" in updateData:
            baseSlug = self.generateSlug(
                updateData["companyName"]
            )

            newSlug = baseSlug

            existingSlug = (
                await self.repo.getBySlug(
                    baseSlug
                )
            )

            if (
                existingSlug
                and existingSlug.id != website.id
            ):
                newSlug = (
                    f"{baseSlug}-"
                    f"{str(uuid.uuid4())[:8]}"
                )

            updateData["slug"] = newSlug

        result = await self.repo.update(
            website,
            updateData,
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def submitWebsite(
        self,
        websiteId: uuid.UUID,
    ) -> Website:

        website = await self.getWebsite(
            websiteId
        )

        if website.status not in (
            "DRAFT",
            "REJECTED",
        ):
            raise ConflictError(
                f"Website cannot be submitted "
                f"from status '{website.status}'"
            )

        if not website.companyName:
            raise ConflictError(
                "Company name is required before submission"
            )

        if not website.businessType:
            raise ConflictError(
                "Business type is required before submission"
            )

        if not website.slug:
            raise ConflictError(
                "Website slug is required before submission"
            )

        website.status = "PENDING"

        await self.session.commit()
        await self.session.refresh(website)

        return website

    async def listPending(
        self,
    ) -> list[Website]:
        return await self.repo.getByStatus(
            "PENDING"
        )

    async def approveWebsite(
        self,
        websiteId: uuid.UUID,
    ) -> Website:

        website = await self.getWebsite(
            websiteId
        )

        if website.status != "PENDING":
            raise ConflictError(
                f"Website cannot be approved "
                f"from status '{website.status}'"
            )

        # Approval and publishing are separate.
        website.status = "APPROVED"

        await self.session.commit()
        await self.session.refresh(website)

        return website

    async def rejectWebsite(
        self,
        websiteId: uuid.UUID,
    ) -> Website:

        website = await self.getWebsite(
            websiteId
        )

        if website.status != "PENDING":
            raise ConflictError(
                f"Website cannot be rejected "
                f"from status '{website.status}'"
            )

        website.status = "REJECTED"

        await self.session.commit()
        await self.session.refresh(website)

        return website

    async def publishWebsite(
        self,
        websiteId: uuid.UUID,
    ) -> Website:

        website = await self.getWebsite(
            websiteId
        )

        if website.status != "APPROVED":
            raise ConflictError(
                f"Website cannot be published "
                f"from status '{website.status}'. "
                f"Website must be APPROVED first."
            )

        website.status = "LIVE"

        await self.session.commit()
        await self.session.refresh(website)

        return website

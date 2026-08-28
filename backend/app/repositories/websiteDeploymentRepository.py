import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.websiteDeployment import WebsiteDeployment


class WebsiteDeploymentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getById(
        self,
        deploymentId: uuid.UUID,
    ) -> WebsiteDeployment | None:
        result = await self.session.execute(
            select(WebsiteDeployment).where(
                WebsiteDeployment.id == deploymentId
            )
        )
        return result.scalar_one_or_none()

    async def getByStoreId(
        self,
        storeId: uuid.UUID,
    ) -> Sequence[WebsiteDeployment]:
        result = await self.session.execute(
            select(WebsiteDeployment)
            .where(WebsiteDeployment.storeId == storeId)
            .order_by(WebsiteDeployment.createdAt.desc())
        )
        return result.scalars().all()

    async def create(
        self,
        deployment: WebsiteDeployment,
    ) -> WebsiteDeployment:
        self.session.add(deployment)
        await self.session.flush()
        await self.session.refresh(deployment)
        return deployment

    async def update(
        self,
        deployment: WebsiteDeployment,
        data: dict,
    ) -> WebsiteDeployment:
        for key, value in data.items():
            setattr(deployment, key, value)

        await self.session.flush()
        await self.session.refresh(deployment)
        return deployment

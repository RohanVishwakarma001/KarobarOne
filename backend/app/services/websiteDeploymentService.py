import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import (
    ConflictError,
    NotFoundError,
)
from app.db.models.websiteDeployment import WebsiteDeployment
from app.db.models.websitePublishLog import WebsitePublishLog
from app.repositories.websiteDeploymentRepository import (
    WebsiteDeploymentRepository,
)
from app.schemas.websiteDeployment import WebsiteDeploymentCreate


ALLOWED_STATUSES = {
    "PENDING",
    "DEPLOYING",
    "SUCCESS",
    "FAILED",
}


class WebsiteDeploymentService:

    def __init__(self, session: AsyncSession):
        self.repo = WebsiteDeploymentRepository(session)
        self.session = session

    async def _createPublishLog(
        self,
        deployment: WebsiteDeployment,
        status: str,
        message: str | None = None,
    ) -> WebsitePublishLog:
        log = WebsitePublishLog(
            storeId=deployment.storeId,
            deploymentId=deployment.id,
            action="PUBLISH",
            status=status,
            version=deployment.deploymentId,
            message=message,
            publishedAt=(
                datetime.now(timezone.utc)
                if status == "SUCCESS"
                else None
            ),
        )

        self.session.add(log)
        await self.session.flush()

        return log

    async def getById(
        self,
        deploymentId: uuid.UUID,
    ) -> WebsiteDeployment:

        deployment = await self.repo.getById(
            deploymentId
        )

        if not deployment:
            raise NotFoundError(
                "Website deployment",
                str(deploymentId),
            )

        return deployment

    async def getByStoreId(
        self,
        storeId: uuid.UUID,
    ):
        return await self.repo.getByStoreId(
            storeId
        )

    async def create(
        self,
        data: WebsiteDeploymentCreate,
    ) -> WebsiteDeployment:

        provider = data.provider.strip().lower()

        if not provider:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_PROVIDER",
                    "message": "Deployment provider is required.",
                },
            )

        deployment = WebsiteDeployment(
            storeId=data.storeId,
            deploymentId=data.deploymentId,
            provider=provider,
            status="PENDING",
            deploymentUrl=None,
            errorMessage=None,
            startedAt=None,
            completedAt=None,
        )

        result = await self.repo.create(
            deployment
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def startDeployment(
        self,
        deploymentId: uuid.UUID,
    ) -> WebsiteDeployment:

        deployment = await self.getById(
            deploymentId
        )

        if deployment.status not in {
            "PENDING",
            "FAILED",
        }:
            raise ConflictError(
                "Deployment can only start from "
                f"PENDING or FAILED. Current status: "
                f"'{deployment.status}'"
            )

        now = datetime.now(timezone.utc)

        result = await self.repo.update(
            deployment,
            {
                "status": "DEPLOYING",
                "startedAt": now,
                "completedAt": None,
                "errorMessage": None,
            },
        )

        await self._createPublishLog(
            deployment,
            "STARTED",
            "Website deployment started.",
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def markSuccess(
        self,
        deploymentId: uuid.UUID,
        deploymentUrl: str | None = None,
    ) -> WebsiteDeployment:

        deployment = await self.getById(
            deploymentId
        )

        if deployment.status != "DEPLOYING":
            raise ConflictError(
                "Deployment can only succeed from "
                f"DEPLOYING. Current status: "
                f"'{deployment.status}'"
            )

        if not deploymentUrl:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "DEPLOYMENT_URL_REQUIRED",
                    "message": (
                        "deploymentUrl is required "
                        "when marking deployment successful."
                    ),
                },
            )

        result = await self.repo.update(
            deployment,
            {
                "status": "SUCCESS",
                "deploymentUrl": deploymentUrl,
                "completedAt": datetime.now(timezone.utc),
                "errorMessage": None,
            },
        )

        await self._createPublishLog(
            deployment,
            "SUCCESS",
            "Website deployment completed successfully.",
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def markFailed(
        self,
        deploymentId: uuid.UUID,
        errorMessage: str,
    ) -> WebsiteDeployment:

        deployment = await self.getById(
            deploymentId
        )

        if deployment.status != "DEPLOYING":
            raise ConflictError(
                "Deployment can only fail from "
                f"DEPLOYING. Current status: "
                f"'{deployment.status}'"
            )

        if not errorMessage.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "DEPLOYMENT_ERROR_REQUIRED",
                    "message": (
                        "errorMessage is required "
                        "when deployment fails."
                    ),
                },
            )

        result = await self.repo.update(
            deployment,
            {
                "status": "FAILED",
                "completedAt": datetime.now(timezone.utc),
                "errorMessage": errorMessage,
            },
        )

        await self._createPublishLog(
            deployment,
            "FAILED",
            errorMessage,
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def updateStatus(
        self,
        deploymentId: uuid.UUID,
        status: str,
        deploymentUrl: str | None = None,
        errorMessage: str | None = None,
    ) -> WebsiteDeployment:

        status = status.strip().upper()

        if status not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_DEPLOYMENT_STATUS",
                    "message": (
                        f"Unsupported deployment status "
                        f"'{status}'."
                    ),
                    "allowedStatuses": sorted(
                        ALLOWED_STATUSES
                    ),
                },
            )

        if status == "DEPLOYING":
            return await self.startDeployment(
                deploymentId
            )

        if status == "SUCCESS":
            return await self.markSuccess(
                deploymentId,
                deploymentUrl,
            )

        if status == "FAILED":
            return await self.markFailed(
                deploymentId,
                errorMessage or "",
            )

        deployment = await self.getById(
            deploymentId
        )

        if deployment.status != "PENDING":
            raise ConflictError(
                "Only a pending deployment can be "
                "reset to PENDING."
            )

        result = await self.repo.update(
            deployment,
            {
                "status": "PENDING",
                "startedAt": None,
                "completedAt": None,
                "deploymentUrl": None,
                "errorMessage": None,
            },
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result

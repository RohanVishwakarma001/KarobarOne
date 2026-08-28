import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.websiteDeployment import (
    WebsiteDeploymentCreate,
    WebsiteDeploymentResponse,
)
from app.services.websiteDeploymentService import (
    WebsiteDeploymentService,
)


router = APIRouter(
    prefix="/website-deployments",
    tags=["Website Deployments"],
)


@router.post(
    "/",
    response_model=WebsiteDeploymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def createWebsiteDeployment(
    data: WebsiteDeploymentCreate,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteDeploymentService(
        session
    ).create(data)


@router.get(
    "/{deploymentId}",
    response_model=WebsiteDeploymentResponse,
)
async def getWebsiteDeployment(
    deploymentId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteDeploymentService(
        session
    ).getById(deploymentId)


@router.get(
    "/store/{storeId}",
    response_model=list[WebsiteDeploymentResponse],
)
async def listWebsiteDeployments(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteDeploymentService(
        session
    ).getByStoreId(storeId)


@router.post(
    "/{deploymentId}/start",
    response_model=WebsiteDeploymentResponse,
)
async def startWebsiteDeployment(
    deploymentId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteDeploymentService(
        session
    ).startDeployment(deploymentId)


@router.post(
    "/{deploymentId}/success",
    response_model=WebsiteDeploymentResponse,
)
async def markWebsiteDeploymentSuccess(
    deploymentId: uuid.UUID,
    deploymentUrl: str,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteDeploymentService(
        session
    ).markSuccess(
        deploymentId,
        deploymentUrl,
    )


@router.post(
    "/{deploymentId}/failed",
    response_model=WebsiteDeploymentResponse,
)
async def markWebsiteDeploymentFailed(
    deploymentId: uuid.UUID,
    errorMessage: str,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteDeploymentService(
        session
    ).markFailed(
        deploymentId,
        errorMessage,
    )


@router.patch(
    "/{deploymentId}/status",
    response_model=WebsiteDeploymentResponse,
)
async def updateWebsiteDeploymentStatus(
    deploymentId: uuid.UUID,
    deploymentStatus: str,
    deploymentUrl: str | None = None,
    errorMessage: str | None = None,
    session: AsyncSession = Depends(getDb),
):
    return await WebsiteDeploymentService(
        session
    ).updateStatus(
        deploymentId,
        deploymentStatus,
        deploymentUrl,
        errorMessage,
    )

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.websiteAIContent import (
    WebsiteAIContentResponse,
)
from app.schemas.websiteAIGeneration import (
    WebsiteAIGenerateRequest,
)
from app.services.websiteAIGenerationService import (
    WebsiteAIGenerationService,
)


router = APIRouter(
    prefix="/website-ai",
    tags=["Website AI Generation"],
)


@router.post(
    "/generate",
    response_model=WebsiteAIContentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generateWebsiteAIContent(
    data: WebsiteAIGenerateRequest,
    session: AsyncSession = Depends(getDb),
):
    service = WebsiteAIGenerationService(
        session
    )

    return await service.generate(
        storeId=data.storeId,
        contentType=data.contentType,
        instructions=data.instructions,
    )

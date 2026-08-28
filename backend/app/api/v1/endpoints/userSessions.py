# Owner: mousamdas156@gmail.com
"""
Router layer for UserSession.
Exposes endpoints to start, list active, and end login sessions.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.userSession import UserSessionCreate, UserSessionResponse
from app.services.userSessionService import UserSessionService

router = APIRouter(prefix="/users/{userId}/sessions", tags=["User Sessions"])


@router.post("/", response_model=UserSessionResponse, status_code=status.HTTP_201_CREATED)
async def startSession(
    userId: uuid.UUID,
    data: UserSessionCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserSessionService(session)
    return await service.startSession(userId, data)


@router.get("/", response_model=list[UserSessionResponse])
async def listActiveSessions(
    userId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserSessionService(session)
    return await service.listActiveSessions(userId)


@router.patch("/{sessionId}/end", response_model=UserSessionResponse)
async def endSession(
    userId: uuid.UUID,
    sessionId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserSessionService(session)
    return await service.endSession(sessionId)

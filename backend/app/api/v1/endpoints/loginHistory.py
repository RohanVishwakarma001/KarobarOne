# Owner: mousamdas156@gmail.com
"""
Router layer for LoginHistory.
Exposes endpoints to record login attempts and retrieve a user's audit trail.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.loginHistory import LoginHistoryCreate, LoginHistoryResponse
from app.services.loginHistoryService import LoginHistoryService

router = APIRouter(prefix="/login-history", tags=["Login History"])


@router.post("/", response_model=LoginHistoryResponse, status_code=status.HTTP_201_CREATED)
async def recordAttempt(
    data: LoginHistoryCreate,
    db: AsyncSession = Depends(getDb),
):
    """
    """
    service = LoginHistoryService(db)
    return await service.recordAttempt(data)


@router.get("/{userId}", response_model=list[LoginHistoryResponse])
async def getHistory(
    userId: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(getDb),
):
    """
    """
    service = LoginHistoryService(db)
    records, _total = await service.getHistory(userId, skip=skip, limit=limit)
    return records

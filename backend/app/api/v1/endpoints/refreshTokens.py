# Owner: mousamdas156@gmail.com
"""
Router layer for RefreshToken.
Exposes endpoints to issue, list, and revoke JWT refresh tokens.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.refreshToken import RefreshTokenCreate, RefreshTokenResponse
from app.services.refreshTokenService import RefreshTokenService

router = APIRouter(prefix="/users/{userId}/refresh-tokens", tags=["Refresh Tokens"])


@router.post("/", response_model=RefreshTokenResponse, status_code=status.HTTP_201_CREATED)
async def issueToken(
    userId: uuid.UUID,
    data: RefreshTokenCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RefreshTokenService(session)
    return await service.issueToken(userId, data)


@router.get("/", response_model=list[RefreshTokenResponse])
async def listUserTokens(
    userId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RefreshTokenService(session)
    return await service.listUserTokens(userId)


@router.delete("/{tokenId}", response_model=RefreshTokenResponse)
async def revokeToken(
    userId: uuid.UUID,
    tokenId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RefreshTokenService(session)
    return await service.revokeToken(tokenId)

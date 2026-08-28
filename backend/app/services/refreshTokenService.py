# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/refreshTokenService.py — JWT Refresh Token Service
# ================================================================================
# Why this file is used:
#   - Coordinates token lifecycles to enable refresh flows.
#
# What components are inside:
#   - hashToken()             -> Creates token hashes.
#   - RefreshTokenService:
#       - issueToken()        -> Issues long-lived refresh tokens.
#       - listUserTokens()    -> Returns tokens matching users.
#       - revokeToken()       -> Marks tokens revoked.
# ================================================================================
"""
Service layer for RefreshToken.
Handles issuing, looking up, and revoking JWT refresh tokens.
"""

import hashlib
import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.refreshToken import RefreshToken
from app.repositories.refreshTokenRepository import RefreshTokenRepository
from app.repositories.userRepository import UserRepository
from app.schemas.refreshToken import RefreshTokenCreate


def hashToken(rawToken: str) -> str:
    """Hashes a raw refresh token string using SHA-256 before persistence."""
    return hashlib.sha256(rawToken.encode("utf-8")).hexdigest()


class RefreshTokenService:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = RefreshTokenRepository(session)
        self.userRepo = UserRepository(session)
        self.session = session

    async def issueToken(
        self,
        userId: uuid.UUID,
        data: RefreshTokenCreate,
    ) -> RefreshToken:
        """
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))

        token = RefreshToken(
            userId=userId,
            **data.model_dump(),
        )
        result = await self.repo.create(token)
        await self.session.commit()
        return result

    async def listUserTokens(self, userId: uuid.UUID) -> Sequence[RefreshToken]:
        """
        Handles the list user tokens functionality.
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        return await self.repo.getByUserId(userId)

    async def revokeToken(self, tokenId: uuid.UUID) -> RefreshToken:
        """
        Handles the revoke token functionality.
        """
        token = await self.repo.getById(tokenId)
        if not token:
            raise NotFoundError("Refresh token", str(tokenId))
        result = await self.repo.revoke(token)
        await self.session.commit()
        return result
# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/passwordResetTokenService.py — Forgot Password Recovery Service
# ================================================================================
# Why this file is used:
#   - Coordinates forgot-password token creations and changes.
#
# What components are inside:
#   - RESET_TOKEN_TTL_MINUTES -> Token validation lifetimes.
#   - HashToken()            -> Creates token hashes.
#   - PasswordResetTokenService:
#       - requestReset()     -> Generates recovery tokens and saves hashes.
#       - confirmReset()     -> Validates tokens to update user credentials.
# ================================================================================
"""
Service layer for PasswordResetToken.
Handles initiating and completing the forgot-password recovery flow.
"""

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import BusinessValidationError, NotFoundError
from app.db.models.passwordResetToken import PasswordResetToken
from app.repositories.passwordResetTokenRepository import (
    PasswordResetTokenRepository,
)
from app.repositories.userRepository import UserRepository
from app.schemas.passwordResetToken import PasswordResetConfirm, PasswordResetRequest

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

RESET_TOKEN_TTL_MINUTES = 30


def HashToken(rawToken: str) -> str:
    """
    Handles the hash token functionality.
    """
    return hashlib.sha256(rawToken.encode("utf-8")).hexdigest()


class PasswordResetTokenService:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = PasswordResetTokenRepository(session)
        self.userRepo = UserRepository(session)
        self.session = session

    async def requestReset(self, data: PasswordResetRequest) -> str:
        """
        Generates a new password reset token for the user matching the given email.
        Returns the raw (unhashed) token, which the caller is responsible for
        delivering to the user (e.g. via email) — it is never persisted in plaintext.
        """
        user = await self.userRepo.getByEmail(data.email)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", data.email)

        rawToken = secrets.token_urlsafe(32)
        token = PasswordResetToken(
            userId=user.id,
            tokenHash=HashToken(rawToken),
            expiresAt=datetime.now(timezone.utc)
            + timedelta(minutes=RESET_TOKEN_TTL_MINUTES),
        )
        await self.repo.create(token)
        await self.session.commit()
        return rawToken

    async def confirmReset(self, data: PasswordResetConfirm) -> None:
        """
        Validates the raw reset token, then updates the user's password hash.
        """
        tokenHash = HashToken(data.token)
        token = await self.repo.getByTokenHash(tokenHash)
        if not token:
            raise NotFoundError("Password reset token", "invalid token")

        if token.usedAt is not None:
            raise BusinessValidationError("This reset token has already been used")

        if token.expiresAt < datetime.now(timezone.utc):
            raise BusinessValidationError("This reset token has expired")

        user = await self.userRepo.getById(token.userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(token.userId))

        await self.userRepo.update(
            user, {"passwordHash": pwdContext.hash(data.newPassword)}
        )
        await self.repo.markUsed(token)
        await self.session.commit()
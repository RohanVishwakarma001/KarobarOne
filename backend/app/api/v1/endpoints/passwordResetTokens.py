# Owner: mousamdas156@gmail.com
"""
Router layer for PasswordResetToken.
Exposes endpoints to request and confirm a password reset.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.passwordResetToken import (
    PasswordResetConfirm,
    PasswordResetRequest,
)
from app.services.passwordResetTokenService import PasswordResetTokenService

router = APIRouter(prefix="/password-reset", tags=["Password Reset"])


@router.post("/request", status_code=status.HTTP_200_OK)
async def requestReset(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(getDb),
):
    """
    """
    service = PasswordResetTokenService(db)
    # NOTE: The raw token is returned here only as a placeholder for local/dev
    # testing. In production this should be sent via email instead of returned
    # in the response body.
    rawToken = await service.requestReset(data)
    return {"message": "Password reset token generated", "token": rawToken}


@router.post("/confirm", status_code=status.HTTP_200_OK)
async def confirmReset(
    data: PasswordResetConfirm,
    db: AsyncSession = Depends(getDb),
):
    """
    """
    service = PasswordResetTokenService(db)
    await service.confirmReset(data)
    return {"message": "Password has been reset successfully"}

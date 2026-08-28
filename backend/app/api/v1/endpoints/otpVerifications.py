# Owner: mousamdas156@gmail.com
"""
Router layer for OtpVerification.
Exposes endpoints to generate and verify OTP codes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import getSettings
from app.core.exceptionsCompat import BusinessValidationError, NotFoundError
from app.db.session import getDb
from app.schemas.otpVerification import OtpRequest, OtpVerificationResponse, OtpVerify
from app.services.otpVerificationService import OtpVerificationService

router = APIRouter(prefix="/otp", tags=["OTP Verification"])


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generateOtp(
    data: OtpRequest,
    db: AsyncSession = Depends(getDb),
):
    """
    Generates an OTP and emails it to the user's registered address.
    """
    service = OtpVerificationService(db)
    try:
        otp, rawCode = await service.generateOtp(data)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    response = {"message": "OTP sent to registered email", "otpId": otp.id}
    if getSettings().debug:
        # Only surfaced in debug mode — production delivery is via email.
        response["code"] = rawCode
    return response


@router.post("/verify", response_model=OtpVerificationResponse)
async def verifyOtp(
    data: OtpVerify,
    db: AsyncSession = Depends(getDb),
):
    """
    """
    service = OtpVerificationService(db)
    try:
        return await service.verifyOtp(data)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

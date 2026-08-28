# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/otpVerificationService.py — OTP Generation & Verification Service
# ================================================================================
# Why this file is used:
#   - Manages life cycle parameters of one-time password tokens.
#
# What components are inside:
#   - OTP_TTL_MINUTES    -> Expiry period in minutes.
#   - MAX_OTP_ATTEMPTS   -> Failed validation thresholds.
#   - HashOtp()          -> Creates password hashes.
#   - OtpVerificationService:
#       - generateOtp()  -> Generates code strings and saves hashes.
#       - verifyOtp()    -> Evaluates code strings, locking tokens on excess failures.
# ================================================================================
"""
Service layer for OtpVerification.
Handles generating and verifying OTP codes for login, signup, reset, and
transaction flows.
"""

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import BusinessValidationError, NotFoundError
from app.core.mailer import sendEmail
from app.db.models.otpVerification import OtpVerification
from app.db.models.user import User
from app.repositories.otpVerificationRepository import OtpVerificationRepository
from app.repositories.userRepository import UserRepository
from app.schemas.otpVerification import OtpRequest, OtpVerify

OTP_TTL_MINUTES = 10
MAX_OTP_ATTEMPTS = 5

OTP_EMAIL_SUBJECTS = {
    "SIGNUP": "Verify your KarobarOne account",
    "LOGIN": "Your KarobarOne login code",
    "RESET": "Reset your KarobarOne password",
    "TRANSACTION": "Confirm your KarobarOne transaction",
}


def HashOtp(rawCode: str) -> str:
    """
    Handles the hash otp functionality.
    """
    return hashlib.sha256(rawCode.encode("utf-8")).hexdigest()


class OtpVerificationService:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = OtpVerificationRepository(session)
        self.userRepo = UserRepository(session)
        self.session = session

    async def generateOtp(self, data: OtpRequest) -> tuple[OtpVerification, str]:
        """
        Generates a new OTP for the given user and purpose, and emails it to
        the user's registered address.
        Returns the created OTP record and the raw 6-digit code — the raw
        code is never persisted in plaintext and should not be surfaced
        outside of local/dev debugging.
        """
        user = await self.userRepo.getById(data.userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(data.userId))

        rawCode = f"{secrets.randbelow(1000000):06d}"
        otp = OtpVerification(
            userId=data.userId,
            purpose=data.purpose,
            otpHash=HashOtp(rawCode),
            expiresAt=datetime.now(timezone.utc) + timedelta(minutes=OTP_TTL_MINUTES),
        )
        await self.repo.create(otp)
        await self.session.commit()
        self._deliverOtp(user, data.purpose, rawCode)
        return otp, rawCode

    def _deliverOtp(self, user: User, purpose: str, rawCode: str) -> None:
        """
        Emails the raw OTP code to the user. Delivery failures are logged
        and swallowed by sendEmail — they must not fail the request that
        generated the OTP.
        """
        subject = OTP_EMAIL_SUBJECTS.get(purpose, "Your KarobarOne verification code")
        body = (
            f"Hi {user.firstName},\n\n"
            f"Your OTP code is: {rawCode}\n"
            f"This code expires in {OTP_TTL_MINUTES} minutes.\n\n"
            "If you didn't request this, you can safely ignore this email."
        )
        sendEmail(user.email, subject, body)

    async def verifyOtp(self, data: OtpVerify) -> OtpVerification:
        """
        Verifies a raw OTP code against the pending record.
        Increments 'attempts' on every failed try and blocks further checks
        once the 5-attempt cap is reached.
        """
        otp = await self.repo.getById(data.otpId)
        if not otp:
            raise NotFoundError("OTP", str(data.otpId))

        if otp.verifiedAt is not None:
            raise BusinessValidationError("This OTP has already been verified")

        if otp.attempts >= MAX_OTP_ATTEMPTS:
            raise BusinessValidationError("Maximum OTP verification attempts exceeded")

        if otp.expiresAt < datetime.now(timezone.utc):
            raise BusinessValidationError("This OTP has expired")

        if otp.otpHash != HashOtp(data.code):
            await self.repo.incrementAttempts(otp)
            await self.session.commit()
            raise BusinessValidationError("Incorrect OTP code")

        result = await self.repo.markVerified(otp)
        await self.session.commit()
        return result
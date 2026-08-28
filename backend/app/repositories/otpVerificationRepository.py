# Owner: mousamdas156@gmail.com
"""
Repository layer for OtpVerification.
Handles direct database queries for OTP-based verification flows.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.otpVerification import OtpVerification


class OtpVerificationRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, otpId: uuid.UUID) -> OtpVerification | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(OtpVerification).where(OtpVerification.id == otpId)
        )
        return result.scalar_one_or_none()

    async def getLatestPending(
        self,
        userId: uuid.UUID,
        purpose: str,
    ) -> OtpVerification | None:
        """
        """
        result = await self.session.execute(
            select(OtpVerification)
            .where(
                OtpVerification.userId == userId,
                OtpVerification.purpose == purpose,
                OtpVerification.verifiedAt.is_(None),
            )
            .order_by(OtpVerification.createdAt.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def create(self, otp: OtpVerification) -> OtpVerification:
        """
        Handles the create functionality.
        """
        self.session.add(otp)
        await self.session.flush()
        await self.session.refresh(otp)
        return otp

    async def incrementAttempts(self, otp: OtpVerification) -> OtpVerification:
        """
        Handles the increment attempts functionality.
        """
        otp.attempts += 1
        await self.session.flush()
        await self.session.refresh(otp)
        return otp

    async def markVerified(self, otp: OtpVerification) -> OtpVerification:
        """
        Handles the mark verified functionality.
        """
        otp.verifiedAt = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(otp)
        return otp

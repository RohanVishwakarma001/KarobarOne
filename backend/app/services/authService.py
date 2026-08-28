# Owner: mousamdas156@gmail.com
import re
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import (
    AccountLockedError,
    AuthenticationError,
    BusinessValidationError,
)
from app.core.securityChat import create_access_token, hash_password, verify_password
from app.db.models.chatUser import ChatUser
from app.services.userSecuritySettingService import UserSecuritySettingService

class UserRole:
    CUSTOMER = "customer"
    STORE_OWNER = "store_owner"
    SUPPORT_AGENT = "support_agent"

VALID_ROLES = [UserRole.CUSTOMER, UserRole.STORE_OWNER, UserRole.SUPPORT_AGENT]


def validate_password_strength(password: str) -> None:
    """Validate minimum password strength requirement (min 8 chars, upper, digit, special)."""
    if (
        len(password) < 8
        or not re.search(r"[A-Z]", password)
        or not re.search(r"\d", password)
        or not re.search(r"[^a-zA-Z0-9]", password)
    ):
        raise BusinessValidationError(
            "Password must be at least 8 characters long and contain uppercase, numbers, and special characters"
        )


class AuthService:

    @staticmethod
    async def register(session: AsyncSession, name: str, email: str, password: str, role: str, storeId: int | None = None) -> ChatUser:
        if role not in VALID_ROLES:
            raise HTTPException(status_code=400, detail="Invalid role")

        validate_password_strength(password)

        stmt = select(ChatUser).where(ChatUser.email == email)
        res = await session.execute(stmt)
        existing = res.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        if role == UserRole.STORE_OWNER:
            if storeId is None:
                raise HTTPException(
                    status_code=400,
                    detail="storeId is required for store_owner registration"
                )

            stmt = select(ChatUser).where(ChatUser.storeId == storeId)
            res = await session.execute(stmt)
            existingStore = res.scalars().first()
            if existingStore:
                raise HTTPException(
                    status_code=400,
                    detail=f"storeId {storeId} is already registered to another owner"
                )
        else:
            storeId = None

        user = ChatUser(
            name=name,
            email=email,
            password=hash_password(password),
            role=role,
            storeId=storeId
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def login(session: AsyncSession, email: str, password: str) -> dict:
        stmt = select(ChatUser).where(ChatUser.email == email)
        res = await session.execute(stmt)
        user = res.scalars().first()

        if not user:
            raise AuthenticationError("Invalid email or password")

        try:
            if isinstance(user.id, uuid.UUID):
                user_uuid = user.id
            elif isinstance(user.id, int):
                user_uuid = uuid.UUID(int=user.id)
            else:
                user_uuid = uuid.UUID(str(user.id))
        except (ValueError, AttributeError):
            user_uuid = uuid.uuid4()

        sec_service = UserSecuritySettingService(session)

        # Check account lockout before password check via UserSecuritySettingService
        try:
            setting = await sec_service.getOrCreate(user_uuid)
            if setting.accountLockedUntil:
                locked_until = setting.accountLockedUntil
                if locked_until.tzinfo is None:
                    locked_until = locked_until.replace(tzinfo=timezone.utc)
                if locked_until > datetime.now(timezone.utc):
                    raise AccountLockedError("Account is locked due to too many failed login attempts")
        except AccountLockedError:
            raise
        except Exception:
            pass

        # Password check
        if not verify_password(password, user.password):
            try:
                await sec_service.recordFailedLogin(user_uuid)
            except Exception:
                pass
            raise AuthenticationError("Invalid email or password")

        # On successful login, reset failed login count via resetFailedLogin()
        try:
            await sec_service.resetFailedLogin(user_uuid)
        except Exception:
            pass

        token = create_access_token({
            "sub": str(user.id),
            "role": user.role
        })

        return {
            "accessToken": token,
            "tokenType": "bearer",
            "userId": user.id,
            "role": user.role,
            "storeId": user.storeId
        }

# Owner: mousamdas156@gmail.com
"""
Authentication endpoints.

Registration and login are gated behind an emailed OTP:
  - POST /auth/register        -> creates the user, emails a SIGNUP OTP
  - POST /auth/register/verify -> verifies the OTP, marks the email verified,
                                   and issues tokens
  - POST /auth/login           -> checks email+password, emails a LOGIN OTP
  - POST /auth/login/verify    -> verifies the OTP and issues tokens
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import getCurrentUserId
from app.core.exceptions import TokenExpiredError, TokenInvalidError
from app.core.exceptionsCompat import AuthenticationError, BusinessValidationError, ConflictError, NotFoundError
from app.core.security import createAccessToken, createRefreshToken, decodeToken
from app.core.tokenBlacklist import revoke_token
from app.db.models.role import Role
from app.db.models.userRoleMapping import UserRoleMapping
from app.db.session import getDb
from app.schemas.otpVerification import OtpRequest, OtpVerify
from app.schemas.user import UserCreate
from app.services.otpVerificationService import OtpVerificationService
from app.services.userService import UserService


async def _getRoleAssignment(session: AsyncSession, userId: uuid.UUID) -> tuple[str, str | None] | None:
    """
    Looks up the caller's (single, MVP-assumed) role assignment so it can be
    embedded into freshly-issued tokens. Returns (roleCode-lowercased, tenantId)
    or None if the user hasn't been assigned a role yet (e.g. hasn't finished
    business/store onboarding).
    """
    mapping = (
        await session.execute(
            select(UserRoleMapping, Role.roleCode)
            .join(Role, Role.id == UserRoleMapping.roleId)
            .where(UserRoleMapping.userId == userId)
            .limit(1)
        )
    ).first()
    if mapping is None:
        return None
    userRoleMapping, roleCode = mapping
    tenantId = str(userRoleMapping.tenantId) if userRoleMapping.tenantId else None
    return roleCode.lower(), tenantId

router = APIRouter(prefix="/auth", tags=["Authentication"])
securityScheme = HTTPBearer()


# ── Pydantic Schemas ──


class TokenRequest(BaseModel):
    userId: str = Field(..., description="The user ID to generate tokens for", min_length=1)


class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str = "bearer"


class RefreshRequest(BaseModel):
    refreshToken: str = Field(..., description="The refresh token to exchange for a new access token")


class RefreshResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"


class OtpPendingResponse(BaseModel):
    userId: str
    otpId: str
    message: str


class OtpConfirmRequest(BaseModel):
    otpId: str = Field(..., description="The OTP record ID returned by register/login")
    code: str = Field(..., min_length=6, max_length=6, description="The 6-digit code emailed to the user")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


# ── Registration ──

@router.post("/register", response_model=OtpPendingResponse, status_code=201)
async def register(
    userPayload: UserCreate,
    session = Depends(getDb),
):
    """
    Register a new global user and email a SIGNUP OTP. The account has no
    usable tokens until the OTP is confirmed via /auth/register/verify.
    """
    userService = UserService(session)
    try:
        user = await userService.createUser(userPayload)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    otpService = OtpVerificationService(session)
    otp, _rawCode = await otpService.generateOtp(OtpRequest(userId=user.id, purpose="SIGNUP"))

    return OtpPendingResponse(
        userId=str(user.id),
        otpId=str(otp.id),
        message="OTP sent to your registered email. Verify it to activate your account.",
    )


@router.post("/register/verify", response_model=TokenResponse)
async def verifyRegistration(
    payload: OtpConfirmRequest,
    session = Depends(getDb),
):
    """
    Confirms the SIGNUP OTP, marks the email verified, and issues tokens.
    """
    otpService = OtpVerificationService(session)
    try:
        otpId = uuid.UUID(payload.otpId)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid otpId")

    try:
        otp = await otpService.verifyOtp(OtpVerify(otpId=otpId, code=payload.code))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if otp.purpose != "SIGNUP":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This OTP was not issued for registration")

    userService = UserService(session)
    user = await userService.markEmailVerified(otp.userId)

    accessToken = createAccessToken(subject=str(user.id))
    refreshToken = createRefreshToken(subject=str(user.id))

    return TokenResponse(
        accessToken=accessToken,
        refreshToken=refreshToken,
    )


# ── Login ──

@router.post("/login", response_model=OtpPendingResponse)
async def login(
    payload: LoginRequest,
    session = Depends(getDb),
):
    """
    Checks email/password credentials and emails a LOGIN OTP. Tokens are
    only issued once the OTP is confirmed via /auth/login/verify.
    """
    userService = UserService(session)
    try:
        user = await userService.authenticate(payload.email, payload.password)
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    if not user.isEmailVerified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please complete registration first.",
        )

    otpService = OtpVerificationService(session)
    otp, _rawCode = await otpService.generateOtp(OtpRequest(userId=user.id, purpose="LOGIN"))

    return OtpPendingResponse(
        userId=str(user.id),
        otpId=str(otp.id),
        message="OTP sent to your registered email.",
    )


@router.post("/login/verify", response_model=TokenResponse)
async def verifyLogin(
    payload: OtpConfirmRequest,
    session = Depends(getDb),
):
    """
    Confirms the LOGIN OTP and issues tokens.
    """
    otpService = OtpVerificationService(session)
    try:
        otpId = uuid.UUID(payload.otpId)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid otpId")

    try:
        otp = await otpService.verifyOtp(OtpVerify(otpId=otpId, code=payload.code))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if otp.purpose != "LOGIN":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This OTP was not issued for login")

    userService = UserService(session)
    user = await userService.recordLogin(otp.userId)

    assignment = await _getRoleAssignment(session, user.id)
    role, tenantId = assignment if assignment else (None, None)

    accessToken = createAccessToken(subject=str(user.id), role=role, tenantId=tenantId)
    refreshToken = createRefreshToken(subject=str(user.id), role=role, tenantId=tenantId)

    return TokenResponse(
        accessToken=accessToken,
        refreshToken=refreshToken,
    )


# ── Route Handlers ──


@router.post("/token", response_model=TokenResponse)
async def generateTokens(request: TokenRequest):
    """
    Simulate user login/authentication.
    Generates and returns an access token and a refresh token for the provided user ID.
    """
    accessToken = createAccessToken(subject=request.userId)
    refreshToken = createRefreshToken(subject=request.userId)

    return TokenResponse(
        accessToken=accessToken,
        refreshToken=refreshToken,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refreshAccessToken(request: RefreshRequest):
    """
    Exchange a valid refresh token for a new access token.
    """
    try:
        payload = decodeToken(request.refreshToken, expectedType="refresh")
    except (TokenExpiredError, TokenInvalidError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    userId = payload["sub"]

    newAccessToken = createAccessToken(subject=userId)
    return RefreshResponse(accessToken=newAccessToken)


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(securityScheme)):
    """
    Revoke current access token.
    """
    token = credentials.credentials
    try:
        payload = decodeToken(token)
        jti = payload.get("jti")
        if jti:
            revoke_token(jti)
    except Exception:
        pass
    return {"message": "Successfully logged out"}


@router.get("/test-protected")
async def testProtectedRoute(userId: str = Depends(getCurrentUserId)):
    """
    A protected test endpoint that requires a valid JWT access token.
    """
    return {
        "message": "Access granted! You are authenticated.",
        "userId": userId,
    }

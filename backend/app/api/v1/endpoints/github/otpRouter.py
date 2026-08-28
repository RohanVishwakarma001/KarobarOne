from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from app.services.github.otpService import otpService

router = APIRouter(
    prefix="/otp",
    tags=["OTP"]
)


class OTPSendRequest(BaseModel):
    email: str


class OTPVerifyRequest(BaseModel):
    email: str
    otp: str


@router.post("/send")
def sendOTP(
    payload: OTPSendRequest
):
    return otpService.sendOTP(payload.email)


@router.post("/verify")
def verifyOTP(
    payload: OTPVerifyRequest
):
    return otpService.verifyOTP(
        payload.email,
        payload.otp
    )
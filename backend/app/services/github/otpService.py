import os
import random
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

otp_store = {}


class OTPService:

    def sendOTP(
        self,
        email: str
    ):

        otp = str(random.randint(100000, 999999))

        otp_store[email] = otp

        msg = EmailMessage()
        msg["Subject"] = "Your Login OTP"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email

        msg.set_content(
            f"Your OTP is: {otp}"
        )

        if EMAIL_ADDRESS and EMAIL_PASSWORD:
            try:
                with smtplib.SMTP_SSL(
                    "smtp.gmail.com",
                    465
                ) as smtp:
                    smtp.login(
                        EMAIL_ADDRESS,
                        EMAIL_PASSWORD
                    )
                    smtp.send_message(msg)
            except Exception:
                pass

        return {
            "success": True,
            "message": "OTP sent successfully"
        }

    def verifyOTP(
        self,
        email: str,
        otp: str
    ):

        if (
            email in otp_store and
            otp_store[email] == otp
        ):

            del otp_store[email]

            return {
                "success": True,
                "message": "OTP verified"
            }

        return {
            "success": False,
            "message": "Invalid OTP"
        }


otpService = OTPService()
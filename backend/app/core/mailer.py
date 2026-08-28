# ================================================================================
# Module: src/core/mailer.py
# Purpose: Transactional email delivery (OTP codes, etc.) via SMTP
# ================================================================================
"""
Free email delivery utility built on SMTP (e.g. a Gmail app password —
no paid provider required). Used to deliver OTP codes for registration
and login.
"""

import smtplib
from email.message import EmailMessage

import structlog

from app.core.config import getSettings

logger = structlog.get_logger(__name__)


def sendEmail(to: str, subject: str, body: str) -> bool:
    """
    Sends a plain-text email via SMTP.

    Returns True on success, False otherwise. Never raises — a delivery
    failure (or missing SMTP credentials, e.g. in local/dev environments)
    is logged and swallowed so it can't take down the calling request.
    """
    settings = getSettings()
    if not settings.emailAddress or not settings.emailPassword:
        logger.warning("Email not sent: SMTP credentials not configured", to=to, subject=subject)
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{settings.emailFromName} <{settings.emailAddress}>"
    message["To"] = to
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL(settings.smtpHost, settings.smtpPort) as smtp:
            smtp.login(settings.emailAddress, settings.emailPassword)
            smtp.send_message(message)
        return True
    except Exception:
        logger.exception("Failed to send email", to=to, subject=subject)
        return False

# ================================================================================
# Module: src/core/mailer.py
# Purpose: Transactional email delivery (OTP codes, etc.)
# ================================================================================
"""
Email delivery for OTP codes and other transactional mail.

Tries Resend's HTTP API first (https://api.resend.com/emails, port 443),
falling back to raw SMTP only if RESEND_API_KEY isn't set. This order isn't
arbitrary: a live diagnostic against the production Render deployment showed
a raw SMTP connect() to smtp.gmail.com hanging for 2+ minutes instead of
failing — Render's outbound network appears to silently drop SMTP traffic
(a common anti-spam measure on budget hosting tiers) rather than refuse it.
Because sendEmail was being called synchronously from an async route
(app/services/otpVerificationService.py), that hang blocked this
single-worker event loop entirely, freezing every other in-flight request
across the whole app, not just the one that triggered it. HTTP/443 doesn't
have that problem on Render, which is why it's now the primary path.

Both paths return True/False and never raise — a delivery failure must not
fail the request that generated the OTP (see otpVerificationService.py).
"""

import smtplib
from email.message import EmailMessage

import httpx
import structlog

from app.core.config import getSettings

logger = structlog.get_logger(__name__)

# Resend HTTP calls get their own short, explicit timeout for the same
# reason the SMTP fallback below does: no network call in this fail-open
# path should be able to hang the caller (see module docstring).
_HTTP_TIMEOUT_SECONDS = 10
_SMTP_TIMEOUT_SECONDS = 10


def sendEmail(to: str, subject: str, body: str) -> bool:
    """
    Sends a plain-text email. Returns True on success, False otherwise.
    Never raises.
    """
    settings = getSettings()

    if settings.resendApiKey:
        return _sendViaResend(to, subject, body)

    if settings.emailAddress and settings.emailPassword:
        return _sendViaSmtp(to, subject, body)

    logger.warning("Email not sent: neither Resend nor SMTP credentials are configured", to=to, subject=subject)
    return False


def _sendViaResend(to: str, subject: str, body: str) -> bool:
    settings = getSettings()
    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.resendApiKey}"},
            json={
                "from": f"{settings.emailFromName} <{settings.resendFromEmail}>",
                "to": [to],
                "subject": subject,
                "text": body,
            },
            timeout=_HTTP_TIMEOUT_SECONDS,
        )
        if response.status_code >= 400:
            logger.error("Resend email send failed", to=to, subject=subject, status=response.status_code, body=response.text[:500])
            return False
        return True
    except httpx.HTTPError as exc:
        logger.exception("Resend request failed", to=to, subject=subject, error=str(exc))
        return False


def _sendViaSmtp(to: str, subject: str, body: str) -> bool:
    settings = getSettings()
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{settings.emailFromName} <{settings.emailAddress}>"
    message["To"] = to
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL(settings.smtpHost, settings.smtpPort, timeout=_SMTP_TIMEOUT_SECONDS) as smtp:
            smtp.login(settings.emailAddress, settings.emailPassword)
            smtp.send_message(message)
        return True
    except Exception:
        logger.exception("SMTP email send failed", to=to, subject=subject)
        return False

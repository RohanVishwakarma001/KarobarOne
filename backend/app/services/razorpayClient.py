# Fail-closed Razorpay client for the ACTIVE payments router
# (app/api/v1/endpoints/payments.py) — NOT the same object as
# app/services/github/razorpayService.py, which is left alone for the
# deprecated github payment routers.
#
# The old service silently returns a fabricated `order_mock_*` response on
# any error or missing credentials, and unconditionally returns True from
# signature verification when the client wasn't configured — i.e. it fails
# OPEN. With RAZORPAY_KEY_ID/SECRET empty in .env right now, that means any
# payload would currently "verify" against the old routes. This client does
# the opposite: any misconfiguration or gateway error raises, never fakes success.

import hmac
import hashlib
from functools import lru_cache

import razorpay
import structlog

from app.core.config import getSettings
from app.core.exceptions import AppException

logger = structlog.get_logger(__name__)


class PaymentGatewayError(AppException):
    """Razorpay is unreachable, misconfigured, or rejected the request (502)."""

    def __init__(self, message: str = "Payment gateway error") -> None:
        super().__init__(message=message, statusCode=502, errorCode="PAYMENT_GATEWAY_ERROR")


class PaymentGatewayNotConfigured(AppException):
    """RAZORPAY_KEY_ID/SECRET aren't set — a config problem, not a user error (500)."""

    def __init__(self) -> None:
        super().__init__(
            message="Payment gateway is not configured on this server",
            statusCode=500,
            errorCode="PAYMENT_GATEWAY_NOT_CONFIGURED",
        )


class RazorpayClient:
    def __init__(self, keyId: str | None, keySecret: str | None, webhookSecret: str | None) -> None:
        self.keyId = keyId
        self.keySecret = keySecret
        self.webhookSecret = webhookSecret
        self._client = razorpay.Client(auth=(keyId, keySecret)) if keyId and keySecret else None

    def _requireClient(self) -> razorpay.Client:
        if self._client is None:
            raise PaymentGatewayNotConfigured()
        return self._client

    def createOrder(self, amountRupees: "int | float", receipt: str) -> dict:
        client = self._requireClient()
        amountPaise = int(round(float(amountRupees) * 100))
        try:
            return client.order.create({"amount": amountPaise, "currency": "INR", "receipt": receipt})
        except Exception as e:
            logger.error("Razorpay order creation failed", error=str(e), receipt=receipt)
            raise PaymentGatewayError(f"Could not create Razorpay order: {e}") from e

    def verifyCheckoutSignature(self, orderId: str, paymentId: str, signature: str) -> bool:
        """
        Verifies the signature Razorpay Checkout.js hands back to the
        frontend on success: HMAC-SHA256("{order_id}|{payment_id}",
        key_secret) must equal `signature`. Requires real credentials —
        there is no "unconfigured means trust it" path.
        """
        if not self.keySecret:
            raise PaymentGatewayNotConfigured()
        expected = hmac.new(
            key=self.keySecret.encode("utf-8"),
            msg=f"{orderId}|{paymentId}".encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def verifyWebhookSignature(self, rawBody: bytes, signature: str) -> bool:
        """
        Verifies an inbound webhook POST: HMAC-SHA256(raw request body,
        webhook secret) must equal the X-Razorpay-Signature header. This is
        a DIFFERENT secret and DIFFERENT payload shape than checkout-signature
        verification above — configured separately in the Razorpay dashboard.
        """
        if not self.webhookSecret:
            raise PaymentGatewayNotConfigured()
        expected = hmac.new(key=self.webhookSecret.encode("utf-8"), msg=rawBody, digestmod=hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def refund(self, razorpayPaymentId: str, amountRupees: "float | None" = None) -> dict:
        client = self._requireClient()
        payload = {}
        if amountRupees is not None:
            payload["amount"] = int(round(float(amountRupees) * 100))
        try:
            return client.payment.refund(razorpayPaymentId, payload)
        except Exception as e:
            logger.error("Razorpay refund failed", error=str(e), razorpayPaymentId=razorpayPaymentId)
            raise PaymentGatewayError(f"Could not process refund: {e}") from e


@lru_cache
def getRazorpayClient() -> RazorpayClient:
    settings = getSettings()
    return RazorpayClient(
        keyId=settings.razorpayKeyId or None,
        keySecret=settings.razorpayKeySecret or None,
        webhookSecret=settings.razorpayWebhookSecret or None,
    )

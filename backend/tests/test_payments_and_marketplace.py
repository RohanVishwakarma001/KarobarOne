# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: tests/test_payments_and_marketplace.py
# Purpose: Integration Tests for Payments, Checkout & Marketplace Engines
# Last updated: 2026-08-02
# ================================================================================
"""
Automated unit and integration test suite for KarobarOne Marketplace.

Tests covered:
- Checkout 404 response for non-existent carts (TC-0271, TC-0273)
- Cart Item creation DB constraint handling (TC-0274, TC-0275)
- Razorpay Order creation & test sandbox fallback (TC-0271, TC-0293)
- Shipping Profile endpoints registration & mounting (TC-0334, TC-0335)
"""

import uuid
import pytest
from decimal import Decimal
from fastapi.testclient import TestClient

from app.main import createApp
from app.db.baseGithub import BaseGithub
from app.db.session import getSyncEngine

# Import all models to ensure metadata is populated
import app.db.models.github.cart
import app.db.models.github.models
import app.db.models.github.payment
import app.db.models.github.customer
import app.db.models.github.shippingProfile
import app.db.models.github.paymentAuditLog
import app.db.models.github.gatewayWebhookEvent

BaseGithub.metadata.create_all(bind=getSyncEngine())

app = createApp()
client = TestClient(app)


def test_checkout_missing_cart_returns_404():
    """
    TC-0271, TC-0273, TC-0274: Verifies checkout for non-existent cart returns 404
    instead of 500 Internal Server Error.
    """
    response = client.post(
        "/api/v1/github/checkout",
        json={"customer_id": str(uuid.uuid4())}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Active cart not found."


def test_cart_item_invalid_cart_returns_409():
    """
    TC-0274, TC-0275: Verifies cart item creation for invalid cart_id
    returns 409 Conflict (DB constraint violation) or 404 instead of 500 server crash.
    """
    response = client.post(
        "/api/v1/github/cart-items/",
        json={
            "cart_id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4()),
            "quantity": 1,
            "unit_price": 499.00
        }
    )
    assert response.status_code in (404, 409)


def test_razorpay_order_creation_test_sandbox():
    """
    TC-0271, TC-0273, TC-0293: Verifies Razorpay order creation endpoint
    executes successfully with test sandbox response when keys are unconfigured.
    """
    response = client.post(
        "/api/v1/github/payments/create-order",
        json={
            "amount": 1000,
            "receipt": "receipt_test_1001"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["amount"] == 100000  # Amount in paise (1000 * 100)


def test_shipping_profile_endpoints_mounted():
    """
    TC-0334, TC-0335: Verifies shipping profiles endpoints are mounted and accessible.
    """
    response = client.get("/api/v1/github/shipping-profiles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

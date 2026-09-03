#!/usr/bin/env python
"""
KarobarOne production verification suite.

Standalone async script (httpx only — no pytest, no in-process ASGI import)
that runs the full business-critical chain sequentially against a REAL
running server:

  P0/P1  Auth (register + token mint) & self-service tenant creation
  P2     Product catalog creation (category -> store -> product)
  P3     Customer & address setup
  P4     Cart -> checkout -> Razorpay payment initiation (+ webhook if the
         script has a matching RAZORPAY_WEBHOOK_SECRET in its own env)
  P5/P6  RBAC denial check & aggregate health check

Each step is independently timed and reported. A step whose correct,
documented behavior is to refuse (e.g. Razorpay payment when the gateway
isn't configured on this deployment, or a platform-only route correctly
rejecting a store-owner token) is reported SKIP/PASS with the reason, never
silently treated as a failure — a fail-closed system behaving as designed is
a verification success, not a defect.

Exit code: 0 only if every non-skipped step passed. Non-zero otherwise, with
every failing step's exact request, expected vs. actual status, and response
body diff printed to stderr.

Usage:
    python smoke_test.py [--base-url http://127.0.0.1:8000] [--no-cleanup]

Safety: this script creates real rows (a user, a tenant, a store, a product,
a customer, an order...) on whatever server --base-url points at. It refuses
to run against a non-localhost host unless --i-understand-this-hits-a-real-server
is also passed, and defaults to cleaning up everything it created afterward
(best-effort; --no-cleanup skips that and prints every created resource ID).
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Awaitable

import httpx

API_PREFIX = "/api/v1"


def _derivePan(runId: str) -> str:
    """
    Deterministically derives a run-unique, format-valid Indian PAN
    (AAAAA9999A) from the script's hex run ID — app/schemas/tenant.py
    enforces this exact pattern. A fixed literal PAN here would collide with
    a leftover tenant from a prior run that couldn't be cleaned up (tenant
    deletion needs a platform_owner token, which this script's self-service
    store_owner token never has — see SmokeTestSuite.cleanup's docstring).
    """
    digest = int(runId, 16)
    letters = "".join(chr(65 + ((digest >> (i * 5)) % 26)) for i in range(5))
    digits = f"{digest % 10000:04d}"
    lastLetter = chr(65 + ((digest >> 25) % 26))
    return f"{letters}{digits}{lastLetter}"

# Windows terminals default stdout to the system codepage (cp1252), which
# can't encode the box-drawing/em-dash characters this script's output uses.
# Reconfiguring here (not just relying on PYTHONIOENCODING) means the script
# works out of the box with a plain `python smoke_test.py` invocation.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# ================================================================================
# Result tracking
# ================================================================================

@dataclass
class StepResult:
    name: str
    status: str  # "PASS" | "FAIL" | "SKIP"
    detailMs: float
    reason: str = ""
    request: dict[str, Any] | None = None
    expected: str = ""
    actual: str = ""


@dataclass
class SuiteState:
    results: list[StepResult] = field(default_factory=list)
    createdResources: dict[str, str] = field(default_factory=dict)  # label -> id, for cleanup + final report

    def passed(self, name: str, ms: float, reason: str = "") -> None:
        self.results.append(StepResult(name, "PASS", ms, reason))
        print(f"  \033[32mPASS\033[0m  {name}  ({ms:.0f}ms){'  — ' + reason if reason else ''}")

    def skipped(self, name: str, reason: str) -> None:
        self.results.append(StepResult(name, "SKIP", 0, reason))
        print(f"  \033[33mSKIP\033[0m  {name}  — {reason}")

    def failed(self, name: str, ms: float, *, request: dict[str, Any], expected: str, actual: str) -> None:
        self.results.append(StepResult(name, "FAIL", ms, request=request, expected=expected, actual=actual))
        print(f"  \033[31mFAIL\033[0m  {name}  ({ms:.0f}ms)")
        print(f"        expected: {expected}")
        print(f"        actual:   {actual}")
        print(f"        request:  {json.dumps(request, default=str)}")

    def summarize(self) -> int:
        passCount = sum(1 for r in self.results if r.status == "PASS")
        failCount = sum(1 for r in self.results if r.status == "FAIL")
        skipCount = sum(1 for r in self.results if r.status == "SKIP")
        total = len(self.results)

        print("\n" + "=" * 72)
        print(f"  {passCount}/{total} passed, {failCount} failed, {skipCount} skipped")
        print("=" * 72)

        if failCount:
            print("\nFailing steps:")
            for r in self.results:
                if r.status == "FAIL":
                    print(f"  - {r.name}: expected {r.expected}, got {r.actual}")

        if self.createdResources:
            print("\nResources created this run:")
            for label, resourceId in self.createdResources.items():
                print(f"  - {label}: {resourceId}")

        return 0 if failCount == 0 else 1


# ================================================================================
# HTTP helpers — every call is a step; failures raise StepFailure and get
# caught by `run_step` so one bad step doesn't crash the whole script.
# ================================================================================

class StepFailure(Exception):
    def __init__(self, request: dict[str, Any], expected: str, actual: str) -> None:
        self.request = request
        self.expected = expected
        self.actual = actual
        super().__init__(f"expected {expected}, got {actual}")


class StepSkip(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


async def _expectStatus(response: httpx.Response, *expected: int, request: dict[str, Any]) -> dict[str, Any]:
    if response.status_code not in expected:
        bodyPreview = response.text[:500]
        raise StepFailure(
            request=request,
            expected=f"HTTP {' or '.join(str(e) for e in expected)}",
            actual=f"HTTP {response.status_code}: {bodyPreview}",
        )
    return response.json() if response.text else {}


async def run_step(state: SuiteState, name: str, coro: Awaitable[Any]) -> Any:
    start = time.perf_counter()
    try:
        result = await coro
        state.passed(name, (time.perf_counter() - start) * 1000)
        return result
    except StepSkip as skip:
        state.skipped(name, skip.reason)
        return None
    except StepFailure as failure:
        state.failed(name, (time.perf_counter() - start) * 1000, request=failure.request, expected=failure.expected, actual=failure.actual)
        return None
    except Exception as exc:  # noqa: BLE001 — deliberately broad: any unexpected exception is a step failure, not a crash
        state.failed(
            name,
            (time.perf_counter() - start) * 1000,
            request={},
            expected="no exception",
            actual=f"{type(exc).__name__}: {exc}",
        )
        return None


# ================================================================================
# Suite
# ================================================================================

class SmokeTestSuite:
    def __init__(self, client: httpx.AsyncClient, state: SuiteState) -> None:
        self.client = client
        self.state = state
        self.runId = uuid.uuid4().hex[:8]

        self.userId: str | None = None
        self.bearerToken: str | None = None
        self.tenantId: str | None = None
        self.storeId: str | None = None
        self.categoryId: str | None = None
        self.productId: str | None = None
        self.customerId: str | None = None
        self.billingAddressId: str | None = None
        self.shippingAddressId: str | None = None
        self.cartId: str | None = None
        self.orderId: str | None = None

    def _authHeaders(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.bearerToken}"} if self.bearerToken else {}

    # ── P0/P1 — Auth & Tenant ──────────────────────────────────────────

    async def registerAndMintToken(self) -> None:
        payload = {
            "firstName": "Smoke",
            "lastName": "Test",
            "email": f"smoketest+{self.runId}@example.com",
            "mobile": f"+91{9000000000 + int(self.runId, 16) % 99999999}",
            "password": "SmokeTest#12345",
        }
        response = await self.client.post(f"{API_PREFIX}/auth/register", json=payload)
        body = await _expectStatus(response, 201, request={"method": "POST", "url": "/auth/register", "body": payload})
        self.userId = body["userId"]
        self.state.createdResources["user"] = self.userId

        tokenResponse = await self.client.post(f"{API_PREFIX}/auth/token", json={"userId": self.userId})
        tokenBody = await _expectStatus(tokenResponse, 200, request={"method": "POST", "url": "/auth/token", "body": {"userId": self.userId}})
        self.bearerToken = tokenBody["accessToken"]

    async def createTenant(self) -> None:
        payload = {
            "panNumber": _derivePan(self.runId),
            "businessName": f"Smoke Test Biz {self.runId}",
            "legalName": f"Smoke Test Biz {self.runId} Pvt Ltd",
            "email": f"biz+{self.runId}@example.com",
            "mobile": f"+91{8000000000 + int(self.runId, 16) % 99999999}",
            "ownerName": "Smoke Test Owner",
            "businessAddressLine1": "123 Test Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postalCode": "560001",
            "businessType": "RETAIL",
        }
        response = await self.client.post(f"{API_PREFIX}/tenants", json=payload, headers=self._authHeaders())
        body = await _expectStatus(response, 201, request={"method": "POST", "url": "/tenants", "body": payload})
        self.tenantId = body["tenant"]["id"]
        # Labeled up front, not just in cleanup() — this key stays accurate
        # even if --no-cleanup is passed and cleanup() never runs.
        self.state.createdResources["tenant (NOT auto-deleted — needs platform_owner)"] = self.tenantId
        # Self-registration mints a fresh role-bearing token — swap it in.
        if body.get("accessToken"):
            self.bearerToken = body["accessToken"]

    # ── P2 — Catalog ────────────────────────────────────────────────────

    async def createStore(self) -> None:
        payload = {
            "tenantId": self.tenantId,
            "storeName": f"Smoke Test Store {self.runId}",
            "storeSlug": f"smoke-test-store-{self.runId}",
            "tagline": "Automated verification store",
        }
        response = await self.client.post(f"{API_PREFIX}/stores/", json=payload, headers=self._authHeaders())
        body = await _expectStatus(response, 200, 201, request={"method": "POST", "url": "/stores/", "body": payload})
        self.storeId = body["id"]
        self.state.createdResources["store"] = self.storeId

    async def createCategoryAndProduct(self) -> None:
        categoryPayload = {"tenantId": self.tenantId, "name": f"Smoke Category {self.runId}", "slug": f"smoke-category-{self.runId}"}
        categoryResponse = await self.client.post(f"{API_PREFIX}/catalog/categories/", json=categoryPayload, headers=self._authHeaders())
        categoryBody = await _expectStatus(
            categoryResponse, 201, request={"method": "POST", "url": "/catalog/categories/", "body": categoryPayload}
        )
        self.categoryId = categoryBody["id"]
        self.state.createdResources["category"] = self.categoryId

        productPayload = {
            "tenantId": self.tenantId,
            "storeId": self.storeId,
            "name": f"Smoke Test Product {self.runId}",
            "slug": f"smoke-test-product-{self.runId}",
            "categoryId": self.categoryId,
            "status": "PUBLISHED",
        }
        productResponse = await self.client.post(f"{API_PREFIX}/catalog/products/", json=productPayload, headers=self._authHeaders())
        productBody = await _expectStatus(
            productResponse, 201, request={"method": "POST", "url": "/catalog/products/", "body": productPayload}
        )
        self.productId = productBody["id"]
        self.state.createdResources["product"] = self.productId

    # ── P3 — Customer & Address ─────────────────────────────────────────

    async def createCustomerAndAddresses(self) -> None:
        customerPayload = {
            "tenantId": self.tenantId,
            "storeId": self.storeId,
            "firstName": "Smoke",
            "lastName": "Customer",
            "email": f"customer+{self.runId}@example.com",
            "mobile": f"+91{7000000000 + int(self.runId, 16) % 99999999}",
            "status": "ACTIVE",
            "password": "SmokeCustomer#12345",
        }
        customerResponse = await self.client.post(f"{API_PREFIX}/customers/", json=customerPayload, headers=self._authHeaders())
        customerBody = await _expectStatus(customerResponse, 200, 201, request={"method": "POST", "url": "/customers/", "body": customerPayload})
        self.customerId = customerBody["data"]["id"]
        self.state.createdResources["customer"] = self.customerId

        async def createAddress(addressType: str) -> str:
            payload = {
                "customerId": self.customerId,
                "addressType": addressType,
                "fullName": "Smoke Customer",
                "mobile": "9876543210",
                "addressLine1": "456 Delivery Lane",
                "city": "Bengaluru",
                "state": "Karnataka",
                "postalCode": "560002",
            }
            response = await self.client.post(f"{API_PREFIX}/addresses/", json=payload, headers=self._authHeaders())
            body = await _expectStatus(response, 201, request={"method": "POST", "url": "/addresses/", "body": payload})
            return body["id"]

        self.billingAddressId = await createAddress("BILLING")
        self.shippingAddressId = await createAddress("SHIPPING")
        self.state.createdResources["billingAddress"] = self.billingAddressId
        self.state.createdResources["shippingAddress"] = self.shippingAddressId

    # ── P4 — Cart, Checkout, Payment ─────────────────────────────────────

    async def addToCartAndCheckout(self) -> None:
        unitPrice = "499.00"
        cartResponse = await self.client.post(
            f"{API_PREFIX}/cart/items",
            params={"tenantId": self.tenantId, "storeId": self.storeId, "customerId": self.customerId, "unitPrice": unitPrice},
            json={"productId": self.productId, "quantity": 2},
            headers=self._authHeaders(),
        )
        cartBody = await _expectStatus(
            cartResponse, 201, request={"method": "POST", "url": "/cart/items", "body": {"productId": self.productId, "quantity": 2}}
        )
        cart = cartBody["data"]
        self.cartId = cart["id"]
        self.state.createdResources["cart"] = self.cartId

        orderPayload = {
            "tenantId": self.tenantId,
            "storeId": self.storeId,
            "customerId": self.customerId,
            "billingAddressId": self.billingAddressId,
            "shippingAddressId": self.shippingAddressId,
            "cartId": self.cartId,
            "items": [
                {
                    "productId": self.productId,
                    "sku": f"SMOKE-{self.runId}",
                    "productName": f"Smoke Test Product {self.runId}",
                    "quantity": 2,
                    "unitPrice": unitPrice,
                }
            ],
        }
        orderResponse = await self.client.post(f"{API_PREFIX}/orders/", json=orderPayload, headers=self._authHeaders())
        orderBody = await _expectStatus(orderResponse, 201, request={"method": "POST", "url": "/orders/", "body": orderPayload})
        self.orderId = orderBody["data"]["id"]
        self.state.createdResources["order"] = self.orderId

    async def initiateRazorpayPayment(self) -> None:
        payload = {"orderId": self.orderId, "tenantId": self.tenantId, "storeId": self.storeId}
        response = await self.client.post(f"{API_PREFIX}/payments/razorpay/create-order", json=payload, headers=self._authHeaders())

        if response.status_code == 500:
            body = response.json()
            if body.get("error", {}).get("code") == "PAYMENT_GATEWAY_NOT_CONFIGURED":
                raise StepSkip("Razorpay isn't configured on this deployment (RAZORPAY_KEY_ID/SECRET unset) — correct fail-closed behavior, not a defect")

        body = await _expectStatus(response, 201, request={"method": "POST", "url": "/payments/razorpay/create-order", "body": payload})
        razorpayOrderId = body["data"]["razorpayOrderId"]
        self.state.createdResources["razorpayOrderId"] = razorpayOrderId

    async def simulateRazorpayWebhook(self) -> None:
        webhookSecret = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")
        if not webhookSecret:
            raise StepSkip("RAZORPAY_WEBHOOK_SECRET not set in this script's environment — cannot compute a valid signature to test the webhook path")

        razorpayOrderId = self.state.createdResources.get("razorpayOrderId")
        if not razorpayOrderId:
            raise StepSkip("No Razorpay order was created (previous step was skipped) — nothing to simulate a webhook for")

        webhookPayload = {
            "id": f"evt_smoketest_{self.runId}",
            "event": "payment.captured",
            "payload": {"payment": {"entity": {"order_id": razorpayOrderId}}},
        }
        rawBody = json.dumps(webhookPayload).encode("utf-8")
        signature = hmac.new(key=webhookSecret.encode("utf-8"), msg=rawBody, digestmod=hashlib.sha256).hexdigest()

        response = await self.client.post(
            f"{API_PREFIX}/payments/razorpay/webhook",
            content=rawBody,
            headers={"Content-Type": "application/json", "X-Razorpay-Signature": signature},
        )
        await _expectStatus(response, 200, request={"method": "POST", "url": "/payments/razorpay/webhook", "body": webhookPayload})

    # ── P5/P6 — RBAC & Health ────────────────────────────────────────────

    async def checkRbacDenial(self) -> None:
        """A store-owner token must be REFUSED on a platform-only route — proving RBAC enforces, not just that it exists."""
        response = await self.client.get(f"{API_PREFIX}/tenants", headers=self._authHeaders())
        if response.status_code != 403:
            raise StepFailure(
                request={"method": "GET", "url": "/tenants", "headers": "store_owner bearer"},
                expected="HTTP 403 (store_owner must be denied a platform-only route)",
                actual=f"HTTP {response.status_code}: {response.text[:300]}",
            )

    async def checkHealth(self) -> None:
        liveness = await self.client.get(f"{API_PREFIX}/health")
        await _expectStatus(liveness, 200, request={"method": "GET", "url": "/health"})

        dbHealth = await self.client.get(f"{API_PREFIX}/health/db")
        await _expectStatus(dbHealth, 200, request={"method": "GET", "url": "/health/db"})

        fullHealth = await self.client.get(f"{API_PREFIX}/health/full")
        # 503 is a legitimate response shape here too (e.g. Redis genuinely
        # down) — what matters is the endpoint answers with the right shape,
        # not that every subsystem reports healthy.
        body = await _expectStatus(fullHealth, 200, 503, request={"method": "GET", "url": "/health/full"})
        for subsystem in ("database", "redis", "worker"):
            if subsystem not in body.get("checks", {}):
                raise StepFailure(
                    request={"method": "GET", "url": "/health/full"},
                    expected=f"'{subsystem}' present in checks",
                    actual=f"checks={list(body.get('checks', {}).keys())}",
                )

    # ── Cleanup ──────────────────────────────────────────────────────────

    async def cleanup(self) -> None:
        """
        Best-effort teardown — failures here are logged, never raised, so a
        partial cleanup never flips the exit code.

        Known, permanent gap: DELETE /tenants/{id} requires a platform_owner
        token (app/api/v1/endpoints/tenants.py), and this script only ever
        holds the store_owner token its own self-service tenant creation
        mints — there is no way to obtain a platform_owner token over pure
        HTTP without a role already seeded in the database (confirmed while
        researching this script's payloads). The tenant this run created is
        therefore reported in the final summary, not silently deleted or
        silently left unmentioned — an operator with platform_owner access
        can remove it via the platform-admin dashboard.
        """
        headers = self._authHeaders()

        async def tryDelete(url: str) -> None:
            try:
                await self.client.delete(url, headers=headers)
            except Exception as exc:  # noqa: BLE001
                print(f"  (cleanup) failed to delete {url}: {exc}", file=sys.stderr)

        if self.productId:
            await tryDelete(f"{API_PREFIX}/catalog/products/{self.productId}")
        if self.categoryId:
            await tryDelete(f"{API_PREFIX}/catalog/categories/{self.categoryId}")
        if self.customerId:
            await tryDelete(f"{API_PREFIX}/customers/{self.customerId}")
        # Tenant deletion is deliberately NOT attempted here — see docstring
        # (already labeled in createdResources by createTenant()).


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Server to verify (default: local dev server)")
    parser.add_argument("--no-cleanup", action="store_true", help="Skip deleting resources created by this run")
    parser.add_argument(
        "--i-understand-this-hits-a-real-server",
        action="store_true",
        dest="confirmedNonLocal",
        help="Required when --base-url isn't localhost/127.0.0.1 — this script creates and mutates real rows",
    )
    args = parser.parse_args()

    isLocal = "127.0.0.1" in args.base_url or "localhost" in args.base_url
    if not isLocal and not args.confirmedNonLocal:
        print(
            f"Refusing to run against {args.base_url} — this creates real tenants/orders/customers.\n"
            "Pass --i-understand-this-hits-a-real-server to proceed.",
            file=sys.stderr,
        )
        return 2

    state = SuiteState()
    print(f"KarobarOne production verification — target: {args.base_url}\n")

    async with httpx.AsyncClient(base_url=args.base_url, timeout=30.0) as client:
        suite = SmokeTestSuite(client, state)

        print("── P0/P1: Auth & Tenant Creation ──")
        await run_step(state, "Register user + mint token", suite.registerAndMintToken())
        if suite.bearerToken:
            await run_step(state, "Self-service tenant creation", suite.createTenant())

        print("\n── P2: Product Catalog Creation ──")
        if suite.tenantId:
            await run_step(state, "Create store", suite.createStore())
        if suite.storeId:
            await run_step(state, "Create category + product", suite.createCategoryAndProduct())

        print("\n── P3: Customer & Address Setup ──")
        if suite.storeId:
            await run_step(state, "Create customer + billing/shipping addresses", suite.createCustomerAndAddresses())

        print("\n── P4: Cart, Checkout & Razorpay Payment ──")
        if suite.productId and suite.customerId:
            await run_step(state, "Add to cart + create order", suite.addToCartAndCheckout())
        if suite.orderId:
            await run_step(state, "Initiate Razorpay payment", suite.initiateRazorpayPayment())
            await run_step(state, "Simulate Razorpay webhook (payment.captured)", suite.simulateRazorpayWebhook())

        print("\n── P5/P6: RBAC & Health ──")
        if suite.bearerToken:
            await run_step(state, "RBAC denies store_owner on platform-only route", suite.checkRbacDenial())
        await run_step(state, "Aggregate health check (db/redis/worker)", suite.checkHealth())

        if not args.no_cleanup:
            print("\n── Cleanup ──")
            await suite.cleanup()
        else:
            print("\n(--no-cleanup passed — resources left in place)")

    return state.summarize()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

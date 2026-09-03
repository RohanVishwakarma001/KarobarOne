"""
Contract tests for the ACTIVE /api/v1/customers router
(app/api/v1/endpoints/customers.py) — the four required boundary cases
(401 / 403-equivalent-tenant-isolation / 422 / 404) plus the happy path and
a regression test for the cross-tenant leak this router used to have.
"""

import uuid

from httpx import AsyncClient


async def _create_customer(async_client: AsyncClient, tenant: dict, **overrides) -> dict:
    payload = {
        "tenantId": str(tenant["tenantId"]),
        "storeId": str(tenant["storeId"]),
        "firstName": "Ada",
        "lastName": "Lovelace",
        "email": f"ada-{uuid.uuid4().hex[:8]}@example.com",
        "mobile": "9876543210",
        **overrides,
    }
    res = await async_client.post("/api/v1/customers/", json=payload)
    assert res.status_code == 201, res.text
    return res.json()["data"]


# ── Happy path ────────────────────────────────
async def test_create_then_get_customer(async_client: AsyncClient, staff_access_token: str, test_customer_tenant: dict):
    created = await _create_customer(async_client, test_customer_tenant)
    headers = {"Authorization": f"Bearer {staff_access_token}", "X-Tenant-ID": str(test_customer_tenant["tenantId"])}

    res = await async_client.get(f"/api/v1/customers/{created['id']}", headers=headers)
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["success"] is True
    assert body["data"]["email"] == created["email"]


# ── 401 Unauthorized ──────────────────────────
async def test_list_customers_without_bearer_token_is_401(async_client: AsyncClient, test_customer_tenant: dict):
    res = await async_client.get(
        "/api/v1/customers/", headers={"X-Tenant-ID": str(test_customer_tenant["tenantId"])}
    )
    assert res.status_code == 401
    # NOTE: this is FastAPI's own HTTPBearer(auto_error=True) rejecting the
    # request before any app code runs, so it never reaches
    # appExceptionHandler — the body is the framework's bare
    # {"detail": "..."}", not this app's {"success", "error"} envelope. A
    # bearer token that's present-but-invalid *does* go through
    # TokenInvalidError -> the full envelope (see the 403 tenant-mismatch
    # test in test_variants_contract.py for the same envelope-vs-plain-detail
    # split on a different router).
    assert res.json() == {"detail": "Not authenticated"}


async def test_list_customers_with_garbage_bearer_token_is_401_with_envelope(async_client: AsyncClient, test_customer_tenant: dict):
    res = await async_client.get(
        "/api/v1/customers/",
        headers={"Authorization": "Bearer not-a-real-token", "X-Tenant-ID": str(test_customer_tenant["tenantId"])},
    )
    assert res.status_code == 401
    body = res.json()
    assert body["success"] is False
    assert body["error"]["code"] == "TOKEN_INVALID"


# ── Tenant isolation (this router's equivalent of a 403) ─────
async def test_get_customer_from_a_different_tenant_is_404_not_leaked(
    async_client: AsyncClient, staff_access_token: str, test_customer_tenant: dict
):
    """
    Regression test: before this session's fix, passing a bare `storeId`
    filter on the list endpoint bypassed tenant scoping entirely. This
    checks the read path returns 404 (not the record) when the caller's
    X-Tenant-ID doesn't match the customer's actual tenant.
    """
    created = await _create_customer(async_client, test_customer_tenant)
    other_tenant_id = uuid.uuid4()
    headers = {"Authorization": f"Bearer {staff_access_token}", "X-Tenant-ID": str(other_tenant_id)}

    res = await async_client.get(f"/api/v1/customers/{created['id']}", headers=headers)
    assert res.status_code == 404, res.text


async def test_list_customers_ignores_storeId_bypass_of_tenant_scope(
    async_client: AsyncClient, staff_access_token: str, test_customer_tenant: dict
):
    created = await _create_customer(async_client, test_customer_tenant)
    other_tenant_id = uuid.uuid4()
    headers = {"Authorization": f"Bearer {staff_access_token}", "X-Tenant-ID": str(other_tenant_id)}

    # Same storeId as the real customer, but under a DIFFERENT tenant header —
    # must not return the other tenant's customer.
    res = await async_client.get(
        f"/api/v1/customers/?storeId={test_customer_tenant['storeId']}", headers=headers
    )
    assert res.status_code == 200, res.text
    returned_ids = [c["id"] for c in res.json()["data"]["data"]]
    assert created["id"] not in returned_ids


async def test_missing_tenant_header_is_rejected(async_client: AsyncClient, staff_access_token: str):
    res = await async_client.get(
        "/api/v1/customers/", headers={"Authorization": f"Bearer {staff_access_token}"}
    )
    assert res.status_code == 404  # TenantNotFoundError — see app/core/tenantResolver.py::getTenantId
    assert res.json()["error"]["code"] == "TENANT_NOT_FOUND"


# ── 422 malformed Pydantic payload ────────────
async def test_create_customer_with_invalid_email_is_422(async_client: AsyncClient, test_customer_tenant: dict):
    payload = {
        "tenantId": str(test_customer_tenant["tenantId"]),
        "storeId": str(test_customer_tenant["storeId"]),
        "firstName": "Ada",
        "email": "not-an-email",
        "mobile": "9876543210",
    }
    res = await async_client.post("/api/v1/customers/", json=payload)
    assert res.status_code == 422, res.text
    body = res.json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert any(err["loc"][-1] == "email" for err in body["error"]["details"])


# ── 404 Not Found ──────────────────────────────
async def test_get_nonexistent_customer_is_404(async_client: AsyncClient, staff_access_token: str, test_customer_tenant: dict):
    headers = {"Authorization": f"Bearer {staff_access_token}", "X-Tenant-ID": str(test_customer_tenant["tenantId"])}
    res = await async_client.get(f"/api/v1/customers/{uuid.uuid4()}", headers=headers)
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "NOT_FOUND"

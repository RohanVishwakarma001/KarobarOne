"""
Contract tests for the nested variants router
(app/productsPorted/routers/variants.py::productVariantsRouter) — this is
the module with a real, first-class 403 (tenant mismatch), so it's the
primary carrier of that boundary case; customers_contract covers 401/422/404.
"""

import uuid

from httpx import AsyncClient


def _variant_payload(**overrides) -> dict:
    return {
        "sku": f"SKU-{uuid.uuid4().hex[:8].upper()}",
        "price": 499.0,
        "inventory": 10,
        "attributes": {"Color": "Red", "Size": "M"},
        **overrides,
    }


# ── Happy path ────────────────────────────────
async def test_create_variant_for_product(async_client: AsyncClient, test_product: dict):
    res = await async_client.post(
        f"/api/v1/catalog/products/{test_product['productId']}/variants",
        headers={"X-Tenant-ID": str(test_product["tenantId"])},
        json=_variant_payload(),
    )
    assert res.status_code == 201, res.text
    body = res.json()
    assert body["tenantId"] == str(test_product["tenantId"])
    assert body["productId"] == str(test_product["productId"])


# ── 403 Tenant mismatch ───────────────────────
async def test_create_variant_with_mismatched_tenant_is_403(async_client: AsyncClient, test_product: dict):
    other_tenant_id = uuid.uuid4()
    res = await async_client.post(
        f"/api/v1/catalog/products/{test_product['productId']}/variants",
        headers={"X-Tenant-ID": str(other_tenant_id)},
        json=_variant_payload(),
    )
    assert res.status_code == 403, res.text
    # variants.py raises plain fastapi.HTTPException (not this app's
    # AppException hierarchy), so the body is {"detail": "..."} — see the
    # note in test_customers_contract.py's 401 test for the same split.
    assert "Tenant mismatch" in res.json()["detail"]


# ── 422 malformed Pydantic payload ────────────
async def test_create_variant_with_negative_price_is_422(async_client: AsyncClient, test_product: dict):
    res = await async_client.post(
        f"/api/v1/catalog/products/{test_product['productId']}/variants",
        headers={"X-Tenant-ID": str(test_product["tenantId"])},
        json=_variant_payload(price=-50),
    )
    assert res.status_code == 422, res.text
    body = res.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert any(err["loc"][-1] == "price" for err in body["error"]["details"])


async def test_create_variant_missing_sku_is_422(async_client: AsyncClient, test_product: dict):
    payload = _variant_payload()
    del payload["sku"]
    res = await async_client.post(
        f"/api/v1/catalog/products/{test_product['productId']}/variants",
        headers={"X-Tenant-ID": str(test_product["tenantId"])},
        json=payload,
    )
    assert res.status_code == 422


# ── 404 Not Found ──────────────────────────────
async def test_create_variant_for_nonexistent_product_is_404(async_client: AsyncClient):
    res = await async_client.post(
        f"/api/v1/catalog/products/{uuid.uuid4()}/variants",
        headers={"X-Tenant-ID": str(uuid.uuid4())},
        json=_variant_payload(),
    )
    assert res.status_code == 404


async def test_delete_nonexistent_variant_is_404(async_client: AsyncClient, test_product: dict):
    res = await async_client.delete(
        f"/api/v1/catalog/products/{test_product['productId']}/variants/{uuid.uuid4()}"
    )
    assert res.status_code == 404


# ── 409 duplicate SKU (bonus — the other error case this router was built to guard) ────
async def test_duplicate_sku_is_409(async_client: AsyncClient, test_product: dict):
    headers = {"X-Tenant-ID": str(test_product["tenantId"])}
    payload = _variant_payload(sku="DUP-SKU-TEST")

    first = await async_client.post(f"/api/v1/catalog/products/{test_product['productId']}/variants", headers=headers, json=payload)
    assert first.status_code == 201, first.text

    second = await async_client.post(
        f"/api/v1/catalog/products/{test_product['productId']}/variants",
        headers=headers,
        json=_variant_payload(sku="DUP-SKU-TEST", attributes={"Color": "Blue", "Size": "M"}),
    )
    assert second.status_code == 409, second.text

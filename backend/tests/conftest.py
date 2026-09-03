"""
Shared async test fixtures (httpx.AsyncClient against the real FastAPI app
via ASGITransport — no network socket, no separate server process).

These tests run against whatever DATABASE_URL is configured in .env, same as
the rest of tests/ (there's no test-DB override wired up in this project
yet — see the CI notes in .github/workflows/backend-tests.yml). Every
fixture that creates rows cleans them up itself in a `finally`/teardown so
repeat runs don't accumulate junk data or trip unique constraints.
"""

import uuid
from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.main import app
from app.core.config import getSettings
from app.db.session import getEngine as get_main_engine
from app.productsPorted.core.database import engine as products_engine

settings = getSettings()


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def staff_access_token(async_client: AsyncClient) -> str:
    """
    Mints a valid staff JWT without going through the OTP email flow, using
    /auth/token — a route that exists specifically to "simulate user
    login/authentication" (see its docstring in
    app/api/v1/endpoints/auth.py::generateTokens). Good enough for
    authorization-boundary tests; it is not a substitute for testing the
    real register/login/OTP flow itself.
    """
    res = await async_client.post("/api/v1/auth/token", json={"userId": str(uuid.uuid4())})
    assert res.status_code == 200, res.text
    return res.json()["accessToken"]


@pytest_asyncio.fixture
async def tenant_and_category() -> AsyncIterator[dict]:
    """
    A throwaway tenant id plus a real Category row for it (productsPorted's
    Category has no test-fixture-friendly default path — see
    docs/api-mapping/catalog.md — so tests that need a Product must create
    one directly, bypassing the currently-broken POST /catalog/products/
    default-category auto-provisioning). Cleans up everything it inserts.
    """
    tenant_id = uuid.uuid4()
    store_id = uuid.uuid4()
    unique = uuid.uuid4().hex[:8]

    async with products_engine.begin() as conn:
        category_id = uuid.uuid4()
        await conn.execute(
            text(
                """
                INSERT INTO categories
                    (id, tenant_id, store_id, category_name, category_slug, category_type,
                     display_order, level_number, approval_status, is_system_category, is_active, created_by)
                VALUES
                    (:id, :tenant_id, :store_id, :name, :slug, 'PRODUCT', 0, 0, 'APPROVED', false, true, :created_by)
                """
            ),
            {
                "id": category_id,
                "tenant_id": tenant_id,
                "store_id": store_id,
                "name": f"Test Category {unique}",
                "slug": f"test-category-{unique}",
                "created_by": uuid.uuid4(),
            },
        )

    yield {"tenantId": tenant_id, "storeId": store_id, "categoryId": category_id}

    async with products_engine.begin() as conn:
        await conn.execute(text("DELETE FROM products WHERE tenant_id = :t"), {"t": tenant_id})
        await conn.execute(text("DELETE FROM categories WHERE id = :c"), {"c": category_id})


@pytest_asyncio.fixture
async def test_product(tenant_and_category: dict) -> AsyncIterator[dict]:
    """A real Product row (inserted directly — see tenant_and_category's docstring for why)."""
    product_id = uuid.uuid4()
    unique = uuid.uuid4().hex[:8]

    async with products_engine.begin() as conn:
        await conn.execute(
            text(
                """
                INSERT INTO products
                    (id, tenant_id, store_id, category_id, product_name, product_slug, sku_prefix,
                     product_type_id, status, created_by)
                VALUES
                    (:id, :tenant_id, :store_id, :category_id, :name, :slug, :sku, 1, 'DRAFT', :created_by)
                """
            ),
            {
                "id": product_id,
                "tenant_id": tenant_and_category["tenantId"],
                "store_id": tenant_and_category["storeId"],
                "category_id": tenant_and_category["categoryId"],
                "name": f"Test Product {unique}",
                "slug": f"test-product-{unique}",
                "sku": f"TP-{unique}",
                "created_by": uuid.uuid4(),
            },
        )

    yield {"productId": product_id, **tenant_and_category}
    # products/categories rows are cleaned up by tenant_and_category's teardown.


@pytest_asyncio.fixture
async def test_customer_tenant() -> AsyncIterator[dict]:
    """Throwaway tenant/store pair for the main app's customers table (no FK to a real tenant row required there)."""
    tenant_id = uuid.uuid4()
    store_id = uuid.uuid4()
    yield {"tenantId": tenant_id, "storeId": store_id}
    async with get_main_engine().begin() as conn:
        await conn.execute(text("DELETE FROM customers WHERE tenant_id = :t"), {"t": tenant_id})

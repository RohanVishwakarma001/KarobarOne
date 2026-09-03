# Customers — router mapping

## The three routers

| Router | Prefix | DB model | Table | Status |
|---|---|---|---|---|
| `app/api/v1/endpoints/customers.py` | `/api/v1/customers` | `app.db.models.customers.Customer` | `customers` (main `Base`) | **ACTIVE** |
| `customerEngine/router.py` | `/api/v1/customer-engine` | `EngineCustomer` = **alias of the same** `app.db.models.customers.Customer` class (imported and monkey-patched, not a separate table) | `customers` (same table) | **partially ACTIVE, mostly DEPRECATED** |
| `app/api/v1/endpoints/github/customerRouter.py` | `/api/v1/github/customers` | `app.db.models.github.customer.Customer` — an **independent** SQLAlchemy model on a separate declarative base (`BaseGithub`) | `customers` (same table name, different ORM class) | **DEPRECATED** |

## Why this isn't just "pick one router"

`customerEngine` doesn't have its own customer table — `customerEngine/models.py`
imports the canonical `Customer`/`CustomerAddress` classes and monkey-patches
them at import time (adds `isActive`/`profileImage` hybrid properties, wraps
`__init__`). That mutation is global and process-wide the moment
`customerEngine.router` is imported, which happens unconditionally in
`app/api/router.py`. It's not a data-fork, but it is a shared-mutable-state
hazard — the canonical model's runtime shape now depends on import order and
on a router file that has nothing to do with customer CRUD conceptually.

`app/db/models/github/customer.py`, by contrast, **is** a genuine second
model: its own `BaseGithub` declarative base, its own column set in snake_case
(`first_name`, `customer_code`, ...) mapped 1:1 onto columns that happen to
match the same physical `customers` table by name/type. It reads and writes
the same rows as the canonical model but through a completely independent
ORM mapping with no shared migration lineage. Two independently-evolving
class definitions of one physical table is the actual conflict here, not
just "two URLs for the same thing." `app/db/models/github/order.py` and
`cart.py` store `customer_id` as a bare `UUID` column with **no FK
constraint**, so nothing downstream in `/github/*` actually requires this
model to exist — it's safe to deprecate.

`github/authRouter.py` (`/api/v1/github/auth`) is the same pattern one level
up: synchronous `Session` (not `AsyncSession`) hitting its own `users` table
via `app/services/github/authService.py`, parallel to the main async auth
stack. See `auth.md`.

## What changed in this pass

- `app/api/v1/endpoints/customers.py` rewritten: fully `async`, wraps every
  response in `APIResponse[T]` (`app.schemas.common`), raises `NotFoundError`
  / `ConflictError` / `BadRequestError` (`app.core.exceptions`) instead of
  raw `HTTPException` so error responses go through the global handlers and
  get the same `{success, error}` envelope, and now:
  - always resolves tenant via `Depends(getTenantIdAsUUID)` and filters by it
    — previously, passing a bare `storeId` query param bypassed tenant
    scoping entirely (any caller who knew *any* store's UUID could list its
    customers with no tenant check at all). `storeId` is now an additional
    filter *within* the resolved tenant, not a substitute for it.
  - requires a staff bearer token (`Depends(getCurrentUserId)`) on every
    admin-facing read/write (list, get, update, delete, restore, trash-list,
    get-full). **This is new enforcement on previously-unauthenticated
    endpoints** — confirm the dashboard frontend sends `Authorization: Bearer
    <token>` on these calls before shipping, or they'll start 401ing.
  - `POST /` (registration) is left public/unauthenticated on purpose — it's
    storefront self-registration, not a staff operation.
  - `DELETE /{id}` stays `204 No Content` with no body (HTTP requires an
    empty body on 204), so it's the one endpoint that does **not** use the
    `APIResponse` envelope.
- `customerEngine/router.py`: `GET`/`PUT /customers/{id}` and all four
  `/addresses/*` routes flagged `deprecated=True` — they duplicate
  `/api/v1/customers/{id}` and `/api/v1/addresses/*`. `POST
  /guest-checkout`, `POST /customers/{id}/activate`, and `POST
  /customers/{id}/media` are left **ACTIVE**: no equivalent exists elsewhere
  (guest/registered merge-by-email-or-mobile logic, password-setting account
  activation, mock profile-image upload).
- `github/customerRouter.py` pulled out of the bulk `for r in routers:`
  mount loop in `app/api/v1/endpoints/github/__init__.py` and re-mounted via
  `githubRouter.include_router(customerRouter, deprecated=True)`.

## Not done in this pass (needs a decision, not just a flag)

If anything actually wrote through `/api/v1/github/customers` in production,
those rows live in the same table the canonical model reads — flagging the
router `deprecated=True` stops *new* integrations from reaching for it, it
does not migrate or reconcile existing writes. Before deleting the router
outright, check for production traffic on that path and reconcile any rows
whose `customer_code` prefix or shape doesn't match the canonical
`CUST-XXXXXX` convention.

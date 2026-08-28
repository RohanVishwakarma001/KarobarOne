# KarobarOne Backend

Production-grade, multi-tenant FastAPI backend powering the KarobarOne platform — a SaaS toolkit that lets store owners spin up a tenant workspace, build a storefront/website, manage a product catalog, and run e-commerce operations (carts, checkout, orders, payments, shipping, bookings, coupons, live chat support, AI blog content, and invoicing) end to end.

> This document is generated directly from the current codebase (routers, schemas, models, and services under `app/`) and is kept as the single source of truth for every HTTP endpoint the service exposes. For an always-live, interactive version of the same API, run the server and open the Swagger UI at `/api/v1/docs` (see [Interactive API Docs](#interactive-api-docs)).

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
  - [Project Structure](#project-structure)
  - [Multi-Tenancy](#multi-tenancy)
  - [Request Lifecycle & Middleware](#request-lifecycle--middleware)
  - [Error Handling](#error-handling)
  - [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
  - [Database](#database)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Migrations](#database-migrations)
  - [Running the Server](#running-the-server)
  - [Interactive API Docs](#interactive-api-docs)
- [Authentication & OTP](#authentication--otp)
- [Testing](#testing)
- [Deployment](#deployment)
- [API Reference](#api-reference)
  - [Health](#health)
  - [Authentication](#authentication-endpoints)
  - [OTP Verification (generic)](#otp-verification-generic)
  - [Users](#users)
  - [Roles, Permissions & Access Control](#roles-permissions--access-control)
  - [Tenants & Subscriptions](#tenants--subscriptions)
  - [Catalog: Brands, Categories & Tags](#catalog-brands-categories--tags)
  - [Media & SEO](#media--seo)
  - [Ported Product Catalog (`/catalog`)](#ported-product-catalog-catalog)
  - [Customers](#customers)
  - [Stores & Website Builder](#stores--website-builder)
  - [Approvals, Auditing & Versioning](#approvals-auditing--versioning)
  - [Live Chat](#live-chat)
  - [Invoice Generator](#invoice-generator)
  - [AI Blog Agent](#ai-blog-agent)
  - [Commerce Suite (`/github`): Carts, Orders & Payments](#commerce-suite-github-carts-orders--payments)
  - [Commerce Suite (`/github`): Shipping, Bookings, Offers & Wishlist](#commerce-suite-github-shipping-bookings-offers--wishlist)
  - [Service Engine (`/service-engine`)](#service-engine-service-engine)
  - [Customer Engine (`/customer-engine`)](#customer-engine-customer-engine)
- [Known Issues & Caveats](#known-issues--caveats)
- [Module Ownership](#module-ownership)

---

## Overview

KarobarOne is a multi-tenant backend: many independent stores ("tenants") share one deployment, each with its own users, catalog, website, and orders, isolated by a tenant-resolution layer (header or subdomain). The codebase is organized as one FastAPI application (`app/`) plus two smaller bolt-on engines (`serviceEngine/`, `customerEngine/`) that are mounted into the same app.

At a glance, the platform covers:

- **Identity & access** — global user accounts, OTP-verified registration/login, JWT access/refresh tokens, roles & fine-grained store-staff permissions.
- **Tenants & billing** — tenant workspaces, subscription plans, plan-feature gating, plan history, billing/commission rules, custom domains.
- **Catalog** — brands, categories, tags, a full ported product-catalog module (products/variants/attributes/images/shipping), media management, and SEO metadata.
- **Storefront** — a website builder (themes, sections, deployments, AI-generated content) and a public storefront read API.
- **Commerce** — carts, checkout, orders (with cancellation/return/refund), payments (with gateway settlement/reconciliation), coupons/offers, shipping (including Shiprocket integration), bookings/appointments, wishlists.
- **Support & content** — a live chat system (its own auth), AI-assisted blog content generation, and PDF invoice generation.
- **Governance** — approval workflows, entity versioning/rollback, audit logs, and a review queue.

## Tech Stack

| Layer | Technology |
|---|---|
| Language / runtime | Python 3.11+ |
| Web framework | [FastAPI](https://fastapi.tiangolo.com/) 0.11x, served by [Uvicorn](https://www.uvicorn.org/) |
| ORM / database toolkit | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (async), [Alembic](https://alembic.sqlalchemy.org/) for migrations |
| Database | PostgreSQL (via `asyncpg` + `psycopg2-binary` for sync/Alembic paths); SQLite (`aiosqlite`) supported for local/dev |
| Auth | [PyJWT](https://pyjwt.readthedocs.io/) (HS256 access/refresh tokens), `passlib`/`bcrypt` password hashing |
| Settings | `pydantic-settings` (fail-fast, typed env var loading) |
| Logging | `structlog` (structured JSON in production, colorized console in dev) |
| Email/OTP delivery | Standard library `smtplib` over SMTP (free — a Gmail app password works) |
| Payments | Razorpay SDK |
| AI / content generation | LangGraph, LangChain (Cerebras, Google Gemini, Tavily search) for the blog agent and website AI content |
| File storage | Dropbox SDK (ported product-catalog module) |
| PDF generation | ReportLab (invoice generator) |
| Testing | `pytest`, `pytest-asyncio`, `httpx` |
| Linting | `ruff` |
| Containerization | Docker (`python:3.11-slim`) |

## Architecture

### Project Structure

```
KarobarOne-Backend/
├── app/
│   ├── main.py                  # FastAPI application factory (app.main:app)
│   ├── api/
│   │   ├── router.py             # Aggregates every versioned sub-router
│   │   ├── dependencies.py
│   │   └── v1/endpoints/         # One file (or a few) per resource — ~100 files
│   │       └── github/           # The large ported e-commerce module (~55 routers)
│   ├── core/                     # Config, security, RBAC, middleware, exceptions, mailer, tenancy
│   ├── db/
│   │   ├── models/                # ~49 SQLAlchemy models
│   │   ├── modelsRegistry.py      # Imports every model so Alembic/Base sees them
│   │   └── session.py             # Async (+ sync) engine/session factories
│   ├── schemas/                   # ~49 Pydantic request/response schemas
│   ├── services/                  # Business logic layer, one service per resource
│   ├── repositories/              # Data-access layer (thin query wrappers over models)
│   ├── productsPorted/            # A self-contained ported product-catalog module (own config/schemas/routers)
│   └── apps/                      # Bolt-on apps: blogAgent, invoiceGenerator, live_chat (static UI)
├── serviceEngine/                 # Standalone service-catalog & booking-rules module, mounted at /service-engine
├── customerEngine/                # Standalone guest-checkout/customer-profile module, mounted at /customer-engine
├── alembic/                       # Database migrations
├── tests/                         # pytest test suite
├── Dockerfile / Procfile          # Container & process-manager entry points
└── requirements.txt / pyproject.toml
```

The typical request path for a resource is: **router** (`app/api/v1/endpoints/...`) → **service** (`app/services/...`, business rules) → **repository** (`app/repositories/...`, SQL) → **model** (`app/db/models/...`). The `github/`-prefixed commerce module and the `serviceEngine`/`customerEngine` modules were ported from separate codebases and sometimes inline their logic directly in the router instead of following this layering — see [Known Issues & Caveats](#known-issues--caveats).

### Multi-Tenancy

Every request passes through `TenantMiddleware` (`app/core/tenantResolver.py`), which resolves the active tenant using, in order:

1. An `X-Tenant-ID` request header (highest priority), or
2. The subdomain of the `Host` header (e.g. `acme.karobarone.com` → tenant `acme`). IP-address hosts and a blacklist of common subdomains (`www`, `api`, `admin`, `mail`, `portal`, `dashboard`, `localhost`) are never treated as tenant slugs.

The resolved tenant ID is stored in a request-scoped `ContextVar` (`app/core/tenant.py`), bound to the structured logger for every log line in that request, echoed back in the `X-Tenant-ID` response header, and — when a database session is opened — set as a Postgres session GUC (`app.current_tenant_id`) so row-level security policies (if configured on the database) can use it. Endpoints that require a tenant explicitly can depend on `getTenantId`, which raises a `404 TENANT_NOT_FOUND` if resolution fails.

### Request Lifecycle & Middleware

Applied in this order (outermost first) in `app/main.py`:

1. **`RequestTimingMiddleware`** — measures handler duration, adds `X-Process-Time-Ms` to the response, logs `"Request completed"`.
2. **`RequestIDMiddleware`** — reuses an inbound `X-Request-ID` header or generates a UUID, binds it to structured logging, echoes it back on the response.
3. **`TenantMiddleware`** — see above.
4. **`CORSMiddleware`** — currently `allow_origins=["*"]` with credentials allowed (flagged as a `TODO: Restrict in production` in the source).

### Error Handling

All errors are rendered as JSON. Two shapes exist depending on how the code path raises the error — **check which one applies to the endpoint you're calling** (each entry in the [API Reference](#api-reference) notes this where it matters):

**1. Structured envelope** — automatically produced for any exception that subclasses `AppException` (`app/core/exceptions.py`: `NotFoundError`, `ConflictError`, `BadRequestError`, `UnauthorizedError`, `ForbiddenError`, `TenantNotFoundError`, `TokenExpiredError`, `TokenInvalidError`, and the `exceptionsCompat` variants used by most services):

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tenant with id 'a1b2c3d4-...' not found"
  }
}
```

| errorCode | HTTP status | Raised for |
|---|---|---|
| `NOT_FOUND` | 404 | Resource doesn't exist / soft-deleted |
| `TENANT_NOT_FOUND` | 404 | Tenant couldn't be resolved from header/subdomain |
| `BAD_REQUEST` | 400 | Malformed input, `ValueError`, business-rule violations |
| `CONFLICT` | 409 | Duplicate resource, or a database `IntegrityError` |
| `UNAUTHORIZED` | 401 | Missing/invalid/expired credentials |
| `FORBIDDEN` | 403 | Authenticated but not permitted |
| `VALIDATION_ERROR` | 422 | Pydantic request-body validation failure (includes a `details` array of field errors) |
| `INTERNAL_ERROR` | 500 | Unhandled exception (message is masked — check server logs / `X-Request-ID`) |

**2. Plain FastAPI shape** — many routers (especially the ported `github/` commerce module, `serviceEngine`, `customerEngine`, and several core routers) manually `raise HTTPException(status_code=..., detail="...")` instead of raising an `AppException`, which produces FastAPI's default:

```json
{
  "detail": "Category not found"
}
```

Both shapes can appear even within the same file, since some routers catch a service's `AppException` and re-wrap it in `HTTPException`. When in doubt, treat `"detail"` and `"error.message"` as equally authoritative — the message text is always the useful part.

### Role-Based Access Control (RBAC)

Defined in `app/core/rbac.py`. Roles: `platform_owner`, `platform_staff`, `store_owner`, `store_admin`, `staff`, `customer` (`Roles` class). Three dependency factories gate routes:

- **`require_role(*roles)`** — the caller's JWT `role` claim must be one of the listed roles, else `403`.
- **`require_tenant_match(tenantIdParam="tenantId")`** — the caller's JWT `tenantId` claim must match the `{tenantId}` path parameter (platform-level roles bypass this).
- **`require_permission(code)`** — for `staff`-role users, checks a fine-grained `StoreStaffPermission` row; `platform_owner`/`platform_staff`/`store_owner`/`store_admin` bypass this implicitly.

A route with none of these dependencies (and no plain `Depends(getCurrentUserId)`/`getCurrentUserWithRole)` either) is **public** — callable with no `Authorization` header at all. The [API Reference](#api-reference) marks every route's auth requirement explicitly; a non-trivial number of routes across this codebase are unintentionally public — see [Known Issues & Caveats](#known-issues--caveats).

### Database

- **Async path** (used by almost all of `app/`): SQLAlchemy async engine over `asyncpg`, connection pool tuned via `dbPoolSize`/`dbMaxOverflow`/`dbPoolTimeout`/`dbPoolRecycle`, `pool_pre_ping=True`. `getDb()` (`app/db/session.py`) is the standard FastAPI dependency — it auto-commits on success and auto-rolls-back on any exception.
- **Sync path**: a parallel synchronous engine/session (`getSyncDb()`) exists specifically for the ported `github/` commerce module, which was written against a synchronous session API.
- **Migrations**: Alembic, configured in `alembic/env.py` to import `app.db.modelsRegistry.Base.metadata` and to transparently swap `postgresql+asyncpg://` for `postgresql+psycopg2://` (Alembic itself runs synchronously) or `sqlite+aiosqlite://` for `sqlite://`.

---

## Getting Started

### Prerequisites

- Python 3.11+
- A PostgreSQL database (or use the SQLite default for quick local testing)
- (Optional, for OTP email delivery) A Gmail account with an [app password](https://myaccount.google.com/apppasswords)

### Installation

```bash
git clone <this-repo-url>
cd KarobarOne-Backend

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
# or, using the pyproject.toml + uv.lock (the project also ships a uv lockfile):
# uv sync

cp .env.example .env
# then edit .env with real values (see below)
```

### Environment Variables

Settings are loaded via `pydantic-settings` (`app/core/config.py`) and are **case-sensitive** — the variable names below must match exactly. Everything has a sane default for local development except where marked **required**.

| Variable | Default | Description |
|---|---|---|
| `databaseUrl` | `sqlite+aiosqlite:///./karobar.db` | Main async database connection string |
| `dbPoolSize` / `dbMaxOverflow` / `dbPoolTimeout` / `dbPoolRecycle` | `20` / `10` / `30` / `3600` | Connection pool tuning |
| `jwtSecretKey` | insecure sample value | **Required in production.** HS256 signing key for access/refresh tokens |
| `jwtAlgorithm` | `HS256` | JWT signing algorithm |
| `accessTokenExpireMinutes` | `10080` (7 days) | Access token lifetime |
| `refreshTokenExpireDays` | `7` | Refresh token lifetime |
| `smtpHost` / `smtpPort` | `smtp.gmail.com` / `465` | SMTP server for OTP email delivery |
| `emailAddress` / `emailPassword` | *(empty)* | SMTP login for OTP delivery (see [Authentication & OTP](#authentication--otp)). Without these set, OTPs still generate but delivery silently no-ops. |
| `emailFromName` | `KarobarOne` | Display name on outgoing OTP emails |
| `appName` / `appVersion` | `BackendFoundation` / `0.1.0` | Shown in `/health` and OpenAPI docs |
| `debug` | `false` | Enables SQL echo, Swagger debug mode, and surfaces the raw OTP code in `/api/v1/otp/generate` responses |
| `logLevel` | `INFO` | structlog level |
| `apiPrefix` | `/api/v1` | Prefix under which every router in `app/api/router.py` is mounted |
| `defaultTenantId` / `defaultStoreId` / `defaultUserId` | sample UUIDs | Fallback IDs used by a few modules (e.g. `serviceEngine`) |

Additional environment variables consumed directly via `os.getenv(...)` (not part of the typed `Settings` class — no fail-fast validation, so a typo silently no-ops the feature):

| Variable | Used by | Purpose |
|---|---|---|
| `EMAIL_ADDRESS` / `EMAIL_PASSWORD` | `app/services/github/otpService.py` | **A second, separate** OTP email sender for `/api/v1/github/otp/*` (in-memory OTP store) — distinct from `emailAddress`/`emailPassword` above |
| `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` | `app/services/github/razorpayService.py` | Razorpay payment gateway credentials |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` / `GOOGLE_REDIRECT_URI` | `app/services/github/calendarService.py` | Google Calendar OAuth (booking calendar sync) |
| `SHIPROCKET_EMAIL` / `SHIPROCKET_PASSWORD` / `SHIPROCKET_BASE_URL` | `app/core/configGithub.py` | Shiprocket shipping API credentials |
| `CEREBRAS_API_KEY` | `app/apps/blogAgent/bwaBackend.py` | Cerebras LLM key for the AI blog agent |
| `TAVILY_API_KEY` | Blog agent web-search tool (LangChain Tavily) | Search grounding for blog content |
| `GEMINI_API_KEY` / `GEMINI_MODEL` / `AI_PROVIDER` | `app/services/websiteAIGenerationService.py` | Website AI content generation |
| `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `DROPBOX_ACCESS_TOKEN`, `MAX_IMAGES_PER_PRODUCT`, `MAX_IMAGE_SIZE_BYTES`, `ALLOWED_IMAGE_TYPES` | `app/productsPorted/core/config.py` | A **separate** `Settings` class for the ported product-catalog module. ⚠️ As shipped, this file has hardcoded fallback values baked in for `DATABASE_URL` and `DROPBOX_ACCESS_TOKEN` — treat those as compromised, rotate them, and always set real values via `.env` rather than relying on the file's defaults. |

See `.env.example` for a ready-to-copy template with all of the above.

### Database Migrations

```bash
# Apply all migrations
alembic upgrade head

# Create a new migration after changing models
alembic revision --autogenerate -m "describe the change"

# Roll back one migration
alembic downgrade -1
```

### Running the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The app factory (`createApp()` in `app/main.py`) also mounts a static live-chat UI at `/chat-ui`.

### Interactive API Docs

Once running:

- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`
- Raw OpenAPI schema: `http://localhost:8000/api/v1/openapi.json`

---

## Authentication & OTP

The main platform's identity flow (`app/api/v1/endpoints/auth.py`) issues JWT **access** and **refresh** tokens, and gates both registration and login behind an emailed one-time password. There are three other, unrelated auth systems elsewhere in the codebase (the live-chat `ChatUser` system, the secondary `github/authRouter.py`, and the `customerEngine` guest-checkout flow) — each is documented in its own section of the [API Reference](#api-reference); this section covers only the main platform flow.

**Token usage:** once you have an `accessToken`, send it on every protected request as `Authorization: Bearer <accessToken>`. Access tokens last `accessTokenExpireMinutes` (default 7 days); exchange a `refreshToken` for a new access token via `POST /api/v1/auth/refresh` before it expires. `POST /api/v1/auth/logout` revokes the current access token's `jti` in an in-memory blacklist (`app/core/tokenBlacklist.py` — note this does **not** survive a process restart or work across multiple server instances; it's a single-process blacklist).

**OTP delivery:** OTPs are emailed via SMTP (`app/core/mailer.py`), configured with `smtpHost`/`smtpPort`/`emailAddress`/`emailPassword`/`emailFromName`. A free Gmail account with an [app password](https://myaccount.google.com/apppasswords) works — no paid SMS/email provider required. If `emailAddress`/`emailPassword` are unset, OTP generation still succeeds (email delivery just silently no-ops, logged as a warning) — useful for local development if you also set `debug=true`, which makes `POST /api/v1/otp/generate` echo the raw code back in its response for testing.

### Registration flow

1. **`POST /api/v1/auth/register`** — creates the user record and emails a `SIGNUP` OTP. **No tokens are issued yet.**
2. **`POST /api/v1/auth/register/verify`** — submit the `otpId` (from step 1) and the 6-digit `code` from the email. On success, the user's `isEmailVerified` flag is set and access + refresh tokens are returned.

```
POST /api/v1/auth/register
Content-Type: application/json

{
  "firstName": "Asha",
  "lastName": "Verma",
  "email": "asha@example.com",
  "mobile": "+919876543210",
  "whatsappMobile": "+919876543210",
  "password": "Str0ng!Pass"
}
```

```json
// 201 Created
{
  "userId": "b6d9c9f0-1e2a-4a3b-9c1d-2f3a4b5c6d7e",
  "otpId": "7a8b9c0d-1e2f-4a3b-8c9d-0e1f2a3b4c5d",
  "message": "OTP sent to your registered email. Verify it to activate your account."
}
```

```
POST /api/v1/auth/register/verify
Content-Type: application/json

{
  "otpId": "7a8b9c0d-1e2f-4a3b-8c9d-0e1f2a3b4c5d",
  "code": "483920"
}
```

```json
// 200 OK
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
  "tokenType": "bearer"
}
```

Error examples (both plain `HTTPException` shapes, raised directly by the router):

```json
// 409 Conflict — POST /auth/register, duplicate email/mobile
{ "detail": "User with email 'asha@example.com' already exists" }
```

```json
// 400 Bad Request — POST /auth/register/verify, wrong code
{ "detail": "Incorrect OTP code" }
```

### Login flow (password + OTP, two-factor)

1. **`POST /api/v1/auth/login`** — submit email + password. If valid **and** the account's email is verified, a `LOGIN` OTP is emailed. **No tokens are issued yet.**
2. **`POST /api/v1/auth/login/verify`** — submit the `otpId` and `code`. On success, tokens are issued and `lastLoginAt` is stamped.

```
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "asha@example.com",
  "password": "Str0ng!Pass"
}
```

```json
// 200 OK
{
  "userId": "b6d9c9f0-1e2a-4a3b-9c1d-2f3a4b5c6d7e",
  "otpId": "3c4d5e6f-7a8b-4c9d-0e1f-2a3b4c5d6e7f",
  "message": "OTP sent to your registered email."
}
```

```
POST /api/v1/auth/login/verify
Content-Type: application/json

{
  "otpId": "3c4d5e6f-7a8b-4c9d-0e1f-2a3b4c5d6e7f",
  "code": "019284"
}
```

```json
// 200 OK
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
  "tokenType": "bearer"
}
```

```json
// 401 Unauthorized — POST /auth/login, wrong password
{ "detail": "Invalid email or password" }
```

```json
// 403 Forbidden — POST /auth/login, email never verified
{ "detail": "Email not verified. Please complete registration first." }
```

### Token refresh & logout

```
POST /api/v1/auth/refresh
Content-Type: application/json

{ "refreshToken": "eyJhbGciOiJIUzI1NiIs..." }
```

```json
// 200 OK
{ "accessToken": "eyJhbGciOiJIUzI1NiIs...", "tokenType": "bearer" }
```

```
POST /api/v1/auth/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

```json
// 200 OK
{ "message": "Successfully logged out" }
```

> **Note:** `POST /api/v1/auth/token` also exists and mints an access+refresh token pair for *any* `userId` string with no credential check at all. It predates the OTP flow above and appears to be a dev/testing stub — treat it as unauthenticated token minting, not a login endpoint. See [Known Issues & Caveats](#known-issues--caveats).

---

## Testing

```bash
pytest
```

Configured via `pyproject.toml` (`asyncio_mode = "auto"`, `testpaths = ["tests"]`). The suite in `tests/` covers tenant/subscription flows, booking/module wiring, change-request approvals, payments/marketplace, audit & security fixes, and a numbered regression suite (`test_tc0101_to_tc0141.py`). Run a single file with `pytest tests/test_tenant_subscription.py -v`.

## Deployment

**Docker:**

```bash
docker build -t karobarone-backend .
docker run -p 8000:8000 --env-file .env karobarone-backend
```

The `Dockerfile` installs `requirements.txt` and runs `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`.

**Process manager (Heroku/Railway-style `Procfile`):**

```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Before deploying, at minimum override `jwtSecretKey`, `databaseUrl`, and lock down `CORSMiddleware`'s `allow_origins` (currently `"*"` — see [Known Issues & Caveats](#known-issues--caveats)). Run `alembic upgrade head` against the target database as part of your release step.

---

## API Reference

All paths below are relative to the server root and already include the global `/api/v1` prefix (or the module's extra prefix, e.g. `/api/v1/github/...` or `/api/v1/catalog/...`) — copy them as-is. **Auth** column values: "Public" = no `Authorization` header needed; "Bearer" = a valid JWT access token is required; "Bearer (role: x, y)" = a JWT whose `role` claim is one of the listed roles.

### Health

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/health` | Public | Liveness probe — returns app name/version/timestamp. Does not touch the database. |
| GET | `/api/v1/health/db` | Public | Readiness probe — runs `SELECT 1`; returns `503` with `{"status":"unhealthy","database":"disconnected","error":"..."}` if the database is unreachable. |

```
GET /api/v1/health
```
```json
{
  "status": "healthy",
  "appName": "KarobarOne",
  "version": "1.0.0",
  "timestamp": "2026-08-28T10:15:00.123456+00:00"
}
```

### Authentication Endpoints

Base path: `/api/v1/auth`. Full worked examples for the OTP-gated flows are in [Authentication & OTP](#authentication--otp) above — this table is the complete route list.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Public | Create a user account; emails a SIGNUP OTP. Returns `{userId, otpId, message}`, no tokens. |
| POST | `/api/v1/auth/register/verify` | Public | Confirm the SIGNUP OTP; marks email verified and issues access + refresh tokens. |
| POST | `/api/v1/auth/login` | Public | Verify email + password; if the email is verified, emails a LOGIN OTP. Returns `{userId, otpId, message}`, no tokens. |
| POST | `/api/v1/auth/login/verify` | Public | Confirm the LOGIN OTP; issues access + refresh tokens and stamps `lastLoginAt`. |
| POST | `/api/v1/auth/token` | Public | ⚠️ Mints an access+refresh token pair for any supplied `userId` with **no credential check**. Dev/testing stub — see [Known Issues](#known-issues--caveats). |
| POST | `/api/v1/auth/refresh` | Public (requires a valid refresh token in the body) | Exchange a refresh token for a new access token. |
| POST | `/api/v1/auth/logout` | Bearer | Revoke the current access token (in-memory blacklist, single-process only). |
| GET | `/api/v1/auth/test-protected` | Bearer | Sample protected route that echoes back the authenticated `userId`. |

### OTP Verification (generic)

Base path: `/api/v1/otp`. This is the underlying, purpose-agnostic OTP primitive that `/auth/register` and `/auth/login` build on top of — it can also be used directly for `RESET` (password reset) or `TRANSACTION` confirmation flows.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/otp/generate` | Public | Generate and email an OTP for a given `userId` + `purpose` (`LOGIN`\|`SIGNUP`\|`RESET`\|`TRANSACTION`). Returns `{message, otpId}`; the raw `code` is included only when `debug=true`. |
| POST | `/api/v1/otp/verify` | Public | Verify a raw code against an `otpId`. Max 5 attempts, 10-minute expiry (`OTP_TTL_MINUTES`/`MAX_OTP_ATTEMPTS` in `app/services/otpVerificationService.py`). |

```
POST /api/v1/otp/generate
Content-Type: application/json

{
  "userId": "b6d9c9f0-1e2a-4a3b-9c1d-2f3a4b5c6d7e",
  "purpose": "RESET"
}
```
```json
// 201 Created
{
  "message": "OTP sent to registered email",
  "otpId": "9f8e7d6c-5b4a-3c2d-1e0f-a9b8c7d6e5f4"
}
```

```
POST /api/v1/otp/verify
Content-Type: application/json

{
  "otpId": "9f8e7d6c-5b4a-3c2d-1e0f-a9b8c7d6e5f4",
  "code": "552018"
}
```
```json
// 200 OK
{
  "id": "9f8e7d6c-5b4a-3c2d-1e0f-a9b8c7d6e5f4",
  "userId": "b6d9c9f0-1e2a-4a3b-9c1d-2f3a4b5c6d7e",
  "purpose": "RESET",
  "expiresAt": "2026-08-28T10:25:00Z",
  "verifiedAt": "2026-08-28T10:16:42Z",
  "attempts": 0,
  "createdAt": "2026-08-28T10:15:00Z"
}
```
```json
// 400 Bad Request — expired/wrong code/max attempts (structured envelope — this router catches BusinessValidationError explicitly)
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "This OTP has expired"
  }
}
```

### Users

Base path: `/api/v1/users`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/users/` | Bearer (role: platform_owner, store_owner, store_admin) | Create a user directly (admin-style creation, bypasses the OTP registration flow). |
| GET | `/api/v1/users/{userId}` | Bearer | Get one active user by ID. |
| GET | `/api/v1/users/` | Bearer | List users (`skip`/`limit` query params, default `limit=20`, max `100`). |
| PATCH | `/api/v1/users/{userId}` | Bearer | Update profile fields (partial update; validates email/mobile uniqueness). |
| DELETE | `/api/v1/users/{userId}` | Bearer (role: platform_owner, store_owner) | Soft-delete a user (stamps `deletedAt`). |

```
POST /api/v1/users/
Authorization: Bearer <accessToken>
Content-Type: application/json

{
  "firstName": "Rohan",
  "lastName": "Shah",
  "email": "rohan.shah@example.com",
  "mobile": "+919812345678",
  "whatsappMobile": null,
  "password": "Str0ng!Pass"
}
```
```json
// 201 Created
{
  "id": "c1d2e3f4-5678-4abc-9def-0123456789ab",
  "firstName": "Rohan",
  "lastName": "Shah",
  "email": "rohan.shah@example.com",
  "mobile": "+919812345678",
  "whatsappMobile": null,
  "isActive": true,
  "isEmailVerified": false,
  "isMobileVerified": false,
  "lastLoginAt": null,
  "createdAt": "2026-08-28T10:15:00Z",
  "updatedAt": "2026-08-28T10:15:00Z"
}
```
```json
// 409 Conflict (structured envelope — service raises ConflictError)
{
  "error": {
    "code": "CONFLICT",
    "message": "User with email 'rohan.shah@example.com' already exists"
  }
}
```
```json
// 404 Not Found — GET/PATCH/DELETE an unknown or soft-deleted userId
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User with id 'c1d2e3f4-...' not found"
  }
}
```

### Roles, Permissions & Access Control

*(file: `tenantTest.py`, router prefix `/tenant`)*

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/tenant/info` | Public | Diagnostic endpoint that reads the active tenant from request context and returns it (or `null`) without enforcing that one is present. |
| GET | `/api/v1/tenant/protected` | Public* | Diagnostic endpoint that resolves the tenant via the `getTenantId` dependency and confirms it matches the value in request context; raises `TenantNotFoundError` (404) if no tenant can be identified from the request. |

\* `getTenantId` resolves *tenant* identity from a header/subdomain, not *user* identity — it isn't gated by a JWT bearer token.

#### Roles
*(router-level dependency: `require_role(PLATFORM_OWNER, STORE_OWNER)` applies to all routes below)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/roles/` | Bearer (role: platform_owner, store_owner) | Create a role definition. |
| GET | `/api/v1/roles/{roleId}` | Bearer (role: platform_owner, store_owner) | Fetch a single role by UUID. |
| GET | `/api/v1/roles/` | Bearer (role: platform_owner, store_owner) | List all roles. |
| PATCH | `/api/v1/roles/{roleId}` | Bearer (role: platform_owner, store_owner) | Partially update a role's fields. |
| DELETE | `/api/v1/roles/{roleId}` | Bearer (role: platform_owner, store_owner) | Delete a role (`204`). |

#### Permissions
*(router-level dependency: `require_role(PLATFORM_OWNER, STORE_OWNER)` applies to all routes below)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/permissions/` | Bearer (role: platform_owner, store_owner) | Create a permission definition. |
| GET | `/api/v1/permissions/{permissionId}` | Bearer (role: platform_owner, store_owner) | Fetch a single permission by UUID. |
| GET | `/api/v1/permissions/` | Bearer (role: platform_owner, store_owner) | List all permissions. |
| PATCH | `/api/v1/permissions/{permissionId}` | Bearer (role: platform_owner, store_owner) | Partially update a permission's fields. |
| DELETE | `/api/v1/permissions/{permissionId}` | Bearer (role: platform_owner, store_owner) | Delete a permission (`204`). |

#### Login History

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/login-history/` | Public | Record a login attempt (success/failure) for audit purposes. |
| GET | `/api/v1/login-history/{userId}` | Public | Paginated audit trail of login attempts for a user (`skip`/`limit`). |

#### Password Reset (global users)

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/password-reset/request` | Public | Generate a password reset token. The raw token is returned directly in the response body (dev/local placeholder — not emailed). |
| POST | `/api/v1/password-reset/confirm` | Public | Validate a reset token and set the new password. |

#### Refresh Tokens
*(router prefix `/users/{userId}/refresh-tokens`)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/users/{userId}/refresh-tokens/` | Public | Issue a new JWT refresh-token record for the user. |
| GET | `/api/v1/users/{userId}/refresh-tokens/` | Public | List all refresh tokens issued to the user. |
| DELETE | `/api/v1/users/{userId}/refresh-tokens/{tokenId}` | Public | Revoke a specific refresh token. |

#### Role Permissions
*(router prefix `/roles/{roleId}/permissions`; `require_role(PLATFORM_OWNER, STORE_OWNER)` applies to all routes)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/roles/{roleId}/permissions/` | Bearer (role: platform_owner, store_owner) | Grant a permission to a role. |
| GET | `/api/v1/roles/{roleId}/permissions/` | Bearer (role: platform_owner, store_owner) | List permissions granted to a role. |
| DELETE | `/api/v1/roles/{roleId}/permissions/{mappingId}` | Bearer (role: platform_owner, store_owner) | Revoke a role-permission mapping (`204`). |

#### Store Staff Permissions
*(router prefix `/users/{userId}/store-permissions`; `require_role(PLATFORM_OWNER, STORE_OWNER)` applies to all routes)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/users/{userId}/store-permissions/` | Bearer (role: platform_owner, store_owner) | Grant a store-level permission override to a user. |
| GET | `/api/v1/users/{userId}/store-permissions/` | Bearer (role: platform_owner, store_owner) | List a user's store-level permission overrides. |
| DELETE | `/api/v1/users/{userId}/store-permissions/{recordId}` | Bearer (role: platform_owner, store_owner) | Revoke a store-level permission override (`204`). |

#### User Roles
*(router prefix `/users/{userId}/roles`; `require_role(PLATFORM_OWNER, STORE_OWNER)` applies to all routes)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/users/{userId}/roles/` | Bearer (role: platform_owner, store_owner) | Assign a role to a user. |
| GET | `/api/v1/users/{userId}/roles/` | Bearer (role: platform_owner, store_owner) | List roles assigned to a user. |
| DELETE | `/api/v1/users/{userId}/roles/{mappingId}` | Bearer (role: platform_owner, store_owner) | Revoke a user-role mapping (`204`). |

#### User Security Settings
*(router prefix `/users/{userId}/security-settings`)*

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/users/{userId}/security-settings/` | Public | Get the user's security config (e.g. lockout state), auto-creating defaults if none exist. |
| PATCH | `/api/v1/users/{userId}/security-settings/` | Public | Partially update the user's security config. |

#### User Sessions
*(router prefix `/users/{userId}/sessions`)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/users/{userId}/sessions/` | Public | Start (record) a new login session. |
| GET | `/api/v1/users/{userId}/sessions/` | Public | List a user's active sessions. |
| PATCH | `/api/v1/users/{userId}/sessions/{sessionId}/end` | Public | End a specific active session. |

> ⚠️ Everything in this section below "Roles"/"Permissions"/"Role Permissions"/"Store Staff Permissions"/"User Roles" is currently **public with no auth dependency** — see [Known Issues & Caveats](#known-issues--caveats).

### Tenants & Subscriptions

#### Tenants

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/tenants` | Bearer (role: platform_owner) | Register a new SaaS tenant profile (validates PAN/GST/mobile formats, email+PAN uniqueness). |
| GET | `/api/v1/tenants` | Bearer (role: platform_owner, platform_staff) | List tenants, paginated, filterable by `city`/`state`/`businessType`. |
| GET | `/api/v1/tenants/{tenantId}` | Bearer (role: platform_owner, platform_staff, store_owner) | Fetch full tenant details including nested domains and current plan mapping. |
| PATCH | `/api/v1/tenants/{tenantId}` | Bearer (role: platform_owner) | Partially update tenant profile fields. |
| DELETE | `/api/v1/tenants/{tenantId}` | Bearer (role: platform_owner) | Delete a tenant (domain/plan mappings cascade). |
| PATCH | `/api/v1/tenants/{tenantId}/status` | Bearer (role: platform_owner) | Update the tenant's status (ACTIVE/SUSPENDED/BLOCKED) by `statusId`. |

#### Statuses

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/statuses` | Public | List tenant status presets. |
| POST | `/api/v1/statuses` | Public | Create a status preset; `409` if the name already exists. |

#### Plans

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/plans` | Public | Create a subscription plan tier; `409` if `planCode` is taken. |
| GET | `/api/v1/plans` | Public | List plans, paginated, `activeOnly` filter. |
| GET | `/api/v1/plans/{planId}` | Public | Fetch a plan with its configured features. |
| PATCH | `/api/v1/plans/{planId}` | Public | Partially update a plan. |
| DELETE | `/api/v1/plans/{planId}` | Public | Delete a plan (fails if active tenant mappings reference it). |

#### Features
*(⚠️ path bug — see [Known Issues](#known-issues--caveats): `features.py` hardcodes absolute `/api/v1/...` paths in its decorators with no router prefix, so under the global `/api/v1` mount the paths actually served are doubled, as shown below)*

| Method | Path (as actually served) | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/api/v1/plans/{planId}/features` | Public | Add a feature/resource limit (e.g. `max_products`) to a plan. |
| GET | `/api/v1/api/v1/plans/{planId}/features` | Public | List features/limits configured for a plan. |
| PATCH | `/api/v1/api/v1/features/{featureId}` | Public | Update a plan feature's values. |
| DELETE | `/api/v1/api/v1/features/{featureId}` | Public | Remove a feature/limit from a plan. |

#### Tenant Plan
*(router prefix `/tenants`)*

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/tenants/{tenantId}/plan` | Public | Assign a plan to a tenant for the first time; `409` if already subscribed. |
| GET | `/api/v1/tenants/{tenantId}/plan` | Public | Fetch a tenant's current active plan mapping. |
| PATCH | `/api/v1/tenants/{tenantId}/plan` | Public | Update an active plan mapping (auto-renew, tier change); logs plan history on tier change. |
| POST | `/api/v1/tenants/{tenantId}/upgrade` | Public | Upgrade to a new plan; sends a "Plan Upgraded" notification. |
| POST | `/api/v1/tenants/{tenantId}/downgrade` | Public | Downgrade to a new plan; sends a "Plan Downgraded" notification. |

#### Plan History
*(router prefix `/tenants`)*

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/tenants/{tenantId}/plan-history` | Public | Paginated audit log of a tenant's plan migrations. |

#### Domains

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/tenants/{tenantId}/domains` | Public | Map a subdomain/custom domain to a tenant; custom domains are gated by the tenant's plan (`PlanGuard`, feature `custom_domain`). |
| GET | `/api/v1/tenants/{tenantId}/domains` | Public | List domain mappings for a tenant. |
| PATCH | `/api/v1/domains/{domainId}` | Public | Partially update a domain record (`isPrimary`, SSL dates). |
| DELETE | `/api/v1/domains/{domainId}` | Public | Remove a domain mapping. |

#### Tenant Settings
*(router prefix `/tenants`)*

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/tenants/{tenantId}/settings` | Public | Get a tenant's configuration (currency/timezone/language), initializing defaults if none exist. |
| PATCH | `/api/v1/tenants/{tenantId}/settings` | Public | Partially update tenant configuration. |

#### Billing Rules
*(⚠️ same path-doubling bug as Features — see [Known Issues](#known-issues--caveats))*

| Method | Path (as actually served) | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/api/v1/plans/{planId}/billing-rules` | Public | Register a billing/commission rule for a plan. |
| GET | `/api/v1/api/v1/plans/{planId}/billing-rules` | Public | List billing rules for a plan. |
| GET | `/api/v1/api/v1/billing-rules/{ruleId}` | Public | Fetch a billing rule. |
| PATCH | `/api/v1/api/v1/billing-rules/{ruleId}` | Public | Update a billing rule. |
| DELETE | `/api/v1/api/v1/billing-rules/{ruleId}` | Public | Delete a billing rule. |
| POST | `/api/v1/api/v1/tenants/{tenantId}/calculate-commission` | Public | Calculate transaction commission owed for a given order `amount`. |

#### Example — Register a Tenant

```
POST /api/v1/tenants
Authorization: Bearer <platform-owner-token>
Content-Type: application/json

{
  "panNumber": "ABCDE1234F",
  "gstNumber": "22ABCDE1234F1Z5",
  "businessName": "Rohan General Store",
  "legalName": "Rohan Retail Pvt Ltd",
  "email": "owner@example.com",
  "mobile": "+919876543210",
  "ownerName": "Rohan Vishwakarma",
  "businessAddressLine1": "12 MG Road",
  "city": "Pune",
  "state": "Maharashtra",
  "country": "India",
  "postalCode": "411001",
  "businessType": "Retail",
  "employeeCount": 5
}
```

```json
// 201 Created
{
  "id": "11111111-1111-1111-1111-111111111111",
  "gstNumber": "22ABCDE1234F1Z5",
  "panNumber": "ABCDE1234F",
  "businessName": "Rohan General Store",
  "legalName": "Rohan Retail Pvt Ltd",
  "email": "owner@example.com",
  "mobile": "+919876543210",
  "ownerName": "Rohan Vishwakarma",
  "city": "Pune",
  "state": "Maharashtra",
  "country": "India",
  "postalCode": "411001",
  "businessType": "Retail",
  "statusId": 2,
  "isActive": true,
  "planMapping": null,
  "domains": [],
  "createdAt": "2026-08-28T10:15:00Z",
  "updatedAt": "2026-08-28T10:15:00Z"
}
```

```json
// 409 Conflict
{ "error": { "code": "CONFLICT", "message": "Tenant with email 'owner@example.com' already exists" } }
```

```json
// 404 Not Found — GET /tenants/{tenantId}
{ "error": { "code": "NOT_FOUND", "message": "Tenant with id '11111111-...' not found" } }
```

#### Example — Create a Subscription Plan

```
POST /api/v1/plans
Content-Type: application/json

{
  "planCode": "PRO_MONTHLY",
  "planName": "Pro Growth Plan",
  "monthlyPrice": 999.00,
  "transactionCommissionPercent": 2.50,
  "isActive": true
}
```

```json
// 201 Created
{
  "id": "44444444-4444-4444-4444-444444444444",
  "planCode": "PRO_MONTHLY",
  "planName": "Pro Growth Plan",
  "monthlyPrice": 999.00,
  "transactionCommissionPercent": 2.50,
  "isActive": true,
  "features": [],
  "createdAt": "2026-08-28T10:20:00Z"
}
```

```json
// 409 Conflict
{ "error": { "code": "CONFLICT", "message": "Plan with code 'PRO_MONTHLY' already exists" } }
```

### Catalog: Brands, Categories & Tags

> ⚠️ Every endpoint in this section is **Public (no auth)** — no route in `brands.py`, `brandApprovals.py`, `categories.py`, `tags.py`, or `tagMappings.py` declares any auth dependency.

#### Brands (Global) — `app/api/v1/endpoints/brands.py`
Errors use the plain `{"detail": "..."}` shape (manual `HTTPException`).

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/brands/` | Public | Create a brand. Auto-generates `brandSlug` from `brandName` if omitted. |
| GET | `/api/v1/brands/` | Public | List brands — filter by `tenantId`, `ownerStoreId`, `verificationStatus`, `isPlatformBrand`, `isActive`, `isRaw`; paginated. |
| GET | `/api/v1/brands/{brandId}` | Public | Get a brand by ID (excludes soft-deleted unless `isRaw=true`). |
| PATCH | `/api/v1/brands/{brandId}` | Public | Update a brand. Setting `verificationStatus=APPROVED` auto-stamps `approvedAt`. |
| DELETE | `/api/v1/brands/{brandId}` | Public | Soft-delete a brand (`204`). |
| GET | `/api/v1/brands/trash/list` | Public | List soft-deleted brands. |
| POST | `/api/v1/brands/{brandId}/restore` | Public | Restore a soft-deleted brand. |

#### Brand Approvals (Global) — `app/api/v1/endpoints/brandApprovals.py`
Manages one store's request to sell/represent another store's brand. Errors use `{"detail": "..."}`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/brand-approvals/` | Public | Create an approval request (validates brand exists, `requestingStoreId != brandOwnerStoreId`, date range). |
| GET | `/api/v1/brand-approvals/` | Public | List requests — filter by `brandId`, `requestingStoreId`, `brandOwnerStoreId`, `requestStatus`. |
| GET | `/api/v1/brand-approvals/{approvalId}` | Public | Get a request by ID. |
| PATCH | `/api/v1/brand-approvals/{approvalId}` | Public | Transition `requestStatus` (`APPROVED`/`REJECTED` stamps `reviewedAt`; `REVOKED` stamps `revokedAt`). |
| DELETE | `/api/v1/brand-approvals/{approvalId}` | Public | Hard-delete a request (`204`). |

#### Categories (Global) — `app/api/v1/endpoints/categories.py`
Generic hierarchical category tree, scoped per store/tenant. Errors use `{"detail": "..."}`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/categories/` | Public | Create a category (auto-slugifies name; validates uniqueness + `parentCategoryId`). |
| GET | `/api/v1/categories/` | Public | Paginated list — filter by `storeId`, `tenantId`, `parentCategoryId`, `categoryType`, `isActive`, `isSystemCategory`. |
| GET | `/api/v1/categories/{categoryId}` | Public | Get a category by ID. |
| PATCH | `/api/v1/categories/{categoryId}` | Public | Update; rejects self-parenting. |
| DELETE | `/api/v1/categories/{categoryId}` | Public | Soft-delete (`204`). |
| GET | `/api/v1/categories/trash/list` | Public | List soft-deleted categories. |
| POST | `/api/v1/categories/{categoryId}/restore` | Public | Restore a soft-deleted category. |

#### Tags — `app/api/v1/endpoints/tags.py`
Generic taggable labels scoped by `tagType` + store. Errors use `{"detail": "..."}`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/tags/` | Public | Create a tag; enforces `(storeId, tagType, tagName)` and `(..., tagSlug)` uniqueness. |
| GET | `/api/v1/tags/` | Public | Paginated list — filter by `storeId`, `tenantId`, `tagType`, `isActive`, `isSystemTag`. |
| GET | `/api/v1/tags/{tag_id}` | Public | Get a tag by ID. |
| PATCH | `/api/v1/tags/{tag_id}` | Public | Update a tag (`storeId` itself cannot change). |
| DELETE | `/api/v1/tags/{tag_id}` | Public | Soft-delete (`204`). |

#### Tag Mappings — `app/api/v1/endpoints/tagMappings.py`
Associates a tag with an arbitrary entity. Errors use `{"detail": "..."}`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/tag-mappings/` | Public | Map a tag to an entity; rejects duplicate `(tagId, entityType, entityId)`. |
| GET | `/api/v1/tag-mappings/` | Public | Paginated list — filter by `tagId`, `entityType`, `entityId`. |
| GET | `/api/v1/tag-mappings/{mapping_id}` | Public | Get a mapping by ID. |
| DELETE | `/api/v1/tag-mappings/{mapping_id}` | Public | Hard-delete (`204`). |

#### Example — Create a Brand

```
POST /api/v1/brands/
Content-Type: application/json

{
  "tenantId": "11111111-1111-1111-1111-111111111111",
  "ownerStoreId": "22222222-2222-2222-2222-222222222222",
  "brandName": "Aurora Textiles",
  "websiteUrl": "https://www.auroratextiles.com",
  "supportEmail": "support@auroratextiles.com",
  "description": "Premium handloom textile brand based in Gujarat, India.",
  "countryOfOrigin": "India",
  "gstNumber": "24ABCDE1234F1Z5",
  "isPlatformBrand": false,
  "createdBy": "33333333-3333-3333-3333-333333333333"
}
```

```json
// 201 Created
{
  "id": "44444444-4444-4444-4444-444444444444",
  "tenantId": "11111111-1111-1111-1111-111111111111",
  "ownerStoreId": "22222222-2222-2222-2222-222222222222",
  "brandName": "Aurora Textiles",
  "brandSlug": "aurora-textiles",
  "verificationStatus": "PENDING",
  "isPlatformBrand": false,
  "isActive": true,
  "approvedBy": null,
  "approvedAt": null,
  "createdAt": "2026-08-28T10:15:00Z",
  "updatedAt": "2026-08-28T10:15:00Z",
  "deletedAt": null
}
```

```json
// 400 Bad Request — duplicate slug/name combination (IntegrityError, caught and re-wrapped)
{ "detail": "Brand slug or owner store brand name combination already exists." }
```

### Media & SEO

> All five routers below delegate to service classes that raise `NotFoundError`/`ConflictError` — errors use the structured `{"error": {"code": ...}}` envelope, unlike most of the Catalog section above.

#### Media Files — `/media-files`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/media-files/` | Public | Register an uploaded asset; `409` on duplicate `checksumHash`. |
| GET | `/api/v1/media-files/{mediaFileId}` | Public | Get a media file by ID. |
| GET | `/api/v1/media-files/` | Public | List media files, optionally by `tenantId`. |
| PATCH | `/api/v1/media-files/{mediaFileId}` | Public | Update attributes; `409` on checksum collision. |
| DELETE | `/api/v1/media-files/{mediaFileId}` | Public | Delete (`?soft=true` by default; `?soft=false` for hard delete). |

#### Media Metadata — `/media-metadata`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/media-metadata/` | Public | Create ALT text/title metadata for a media file. |
| GET | `/api/v1/media-metadata/{metadataId}` | Public | Get by its own ID. |
| GET | `/api/v1/media-metadata/media-file/{mediaFileId}` | Public | Get by parent media file ID. |
| GET | `/api/v1/media-metadata/` | Public | List all metadata records. |
| PATCH | `/api/v1/media-metadata/{metadataId}` | Public | Update a record. |
| DELETE | `/api/v1/media-metadata/{metadataId}` | Public | Hard-delete (`204`). |

#### Media Upload Logs — `/media-upload-logs`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/media-upload-logs/` | Public | Create an upload log entry. |
| GET | `/api/v1/media-upload-logs/{logId}` | Public | Get by ID. |
| GET | `/api/v1/media-upload-logs/` | Public | List, optionally by `mediaFileId`. |
| PATCH | `/api/v1/media-upload-logs/{logId}` | Public | Update an entry. |
| DELETE | `/api/v1/media-upload-logs/{logId}` | Public | Hard-delete (`204`). |

#### Media Variants — `/media-variants`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/media-variants/` | Public | Create a variant (thumbnail/medium/large) for a media file. |
| GET | `/api/v1/media-variants/{variantId}` | Public | Get by ID. |
| GET | `/api/v1/media-variants/` | Public | List, optionally by `mediaFileId`. |
| PATCH | `/api/v1/media-variants/{variantId}` | Public | Update dimensions/storage attributes. |
| DELETE | `/api/v1/media-variants/{variantId}` | Public | Hard-delete (`204`). |

#### SEO Metadata — `/seo-metadata`
CRUD uses the structured envelope; the four AI/analysis utility routes at the bottom are stateless.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/seo-metadata/` | Public | Create an SEO record for an entity. |
| GET | `/api/v1/seo-metadata/{seoId}` | Public | Get by its own ID. |
| GET | `/api/v1/seo-metadata/entity/{entityType}/{entityId}` | Public | Get by entity type + ID. |
| GET | `/api/v1/seo-metadata/slug/{entityType}/{slug}` | Public | Get by entity type + URL slug. |
| GET | `/api/v1/seo-metadata/` | Public | List, optionally by `tenantId`. |
| PATCH | `/api/v1/seo-metadata/{seoId}` | Public | Update search preferences. |
| DELETE | `/api/v1/seo-metadata/{seoId}` | Public | Hard-delete (`204`). |
| POST | `/api/v1/seo-metadata/score` | Public | Calculate an SEO score for supplied content. |
| POST | `/api/v1/seo-metadata/ai-suggestions` | Public | Generate AI-assisted SEO suggestions. |
| POST | `/api/v1/seo-metadata/audit` | Public | Run an SEO audit against content/URL. |
| POST | `/api/v1/seo-metadata/keyword-density` | Public | Analyze keyword density of supplied text. |

### Ported Product Catalog (`/catalog`)

Mounted with an extra `/catalog` prefix on top of `/api/v1` (`app/productsPorted/routers/*.py`). This is a **separate, tenant-scoped** product-catalog implementation with its own `Brand`/`Category` models — distinct from the "Global" Brands/Categories above.

> ⚠️ Every endpoint below is **Public (no auth)**.

#### Catalog Categories — `/catalog/categories`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/catalog/categories/` | Public | Create a category; validates `parentId`, unique `(tenantId, parentId, name)` and `(tenantId, slug)`. |
| GET | `/api/v1/catalog/categories/` | Public | List for a `tenantId` (required), optional `parentId`. |
| GET | `/api/v1/catalog/categories/{categoryId}` | Public | Get by ID. |
| PATCH | `/api/v1/catalog/categories/{categoryId}` | Public | Update; runs a cycle-safety ancestor walk when `parentId` changes. |
| DELETE | `/api/v1/catalog/categories/{categoryId}` | Public | Soft-delete (`204`). |

#### Catalog Products — `/catalog/products`
Plan-limit checks raise `PlanLimitExceeded` (`app/core/planGuard.py`) — an `HTTPException` whose `detail` is a **structured object**, a third error shape distinct from both `{"detail": "<string>"}` and `{"error": {"code": ...}}`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/catalog/products/` | Public | Create a product — enforces the tenant's plan product-count limit, validates `brandId`/`shippingProfileId`, checks SKU/slug uniqueness, blocks publishing to an unapproved brand, writes an `AuditLog`. |
| GET | `/api/v1/catalog/products/{productId}` | Public | Get with nested `category`/`brand`/`shippingProfile`/`variants`/`images`/`attributeMappings`. |
| PATCH | `/api/v1/catalog/products/{productId}` | Public | Update with the same validations, plus an audit diff entry. |
| DELETE | `/api/v1/catalog/products/{productId}` | Public | Soft-delete (`204`) + audit entry. |
| GET | `/api/v1/catalog/products/` | Public | Paginated/sorted search — requires `tenantId`; optional `storeId`, `categoryId`, `brandId`, `status`, `productType`, `search`, `sortBy`, `sortOrder`. |
| POST | `/api/v1/catalog/products/{productId}/submit-approval` | Public | Transition `status` to `PENDING`. |
| POST | `/api/v1/catalog/products/{productId}/approve` | Public | Approve `PENDING` → `PUBLISHED` (fails if brand unapproved). |
| POST | `/api/v1/catalog/products/bulk-import` | Public | Bulk-create from an uploaded CSV (`multipart/form-data`). Returns per-row success/error counts. |

#### Catalog Variants — `/catalog/variants`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/catalog/variants/` | Public | Create a variant; validates product exists, SKU + attribute-combination uniqueness per product. |
| GET | `/api/v1/catalog/variants/` | Public | List for a `productId` (required). |
| GET | `/api/v1/catalog/variants/{variantId}` | Public | Get by ID. |
| PATCH | `/api/v1/catalog/variants/{variantId}` | Public | Update; re-validates uniqueness. |
| DELETE | `/api/v1/catalog/variants/{variantId}` | Public | Hard-delete (`204`). |

#### Catalog Attributes — `/catalog/attributes`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/catalog/attributes/` | Public | Create an attribute master (`text`/`select`/`multi-select`/`boolean`); enforces `(tenantId, code)` uniqueness. |
| GET | `/api/v1/catalog/attributes/` | Public | List for a `tenantId` (required). |
| GET | `/api/v1/catalog/attributes/{attributeId}` | Public | Get by ID. |
| PATCH | `/api/v1/catalog/attributes/{attributeId}` | Public | Update; re-validates `code` uniqueness. |
| DELETE | `/api/v1/catalog/attributes/{attributeId}` | Public | Hard-delete (`204`). |
| POST | `/api/v1/catalog/attributes/mappings` | Public | Link an attribute to a product with a value (rejects a second mapping of the same attribute). |
| GET | `/api/v1/catalog/attributes/mappings/{productId}` | Public | List mappings for a product. |
| DELETE | `/api/v1/catalog/attributes/mappings/{mappingId}` | Public | Remove a mapping (`204`). |

#### Catalog Images — `/catalog/images`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/catalog/images/` | Public | Register an image by URL reference; demotes other `isPrimary` images if this one is primary. |
| POST | `/api/v1/catalog/images/upload` | Public | Upload actual image bytes (`multipart/form-data`); validates magic bytes (rejects executables/HTML/scripts), dedupes by MD5, stores via Dropbox or a mocked URL. |
| GET | `/api/v1/catalog/images/` | Public | List for a `productId` (required). |
| DELETE | `/api/v1/catalog/images/{imageId}` | Public | Hard-delete a reference (`204`). |

#### Catalog Shipping — `/catalog/shipping`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/catalog/shipping/` | Public | Create a shipping profile; enforces unique `(tenantId, name)`. |
| GET | `/api/v1/catalog/shipping/` | Public | List active profiles for a `tenantId` (required). |
| GET | `/api/v1/catalog/shipping/{profileId}` | Public | Get an active profile by ID. |
| PATCH | `/api/v1/catalog/shipping/{profileId}` | Public | Update; re-validates name uniqueness. |
| DELETE | `/api/v1/catalog/shipping/{profileId}` | Public | Deactivate (`204`, `isActive=false` — not a hard delete). |

#### Catalog Brands & Approvals — `/catalog/brands`
**Distinct from the global Brands API** — this module's own simpler `Brand` model plus an approval-request workflow.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/catalog/brands/` | Public | Create a catalog brand; enforces unique `(tenantId, name)`. |
| GET | `/api/v1/catalog/brands/` | Public | List for a `tenantId` (required). |
| GET | `/api/v1/catalog/brands/{brandId}` | Public | Get by ID. |
| PATCH | `/api/v1/catalog/brands/{brandId}` | Public | Update; re-validates name uniqueness. |
| DELETE | `/api/v1/catalog/brands/{brandId}` | Public | Soft-delete (`204`). |
| POST | `/api/v1/catalog/brands/{brandId}/request-approval` | Public | Submit an approval request (rejects if one is already `PENDING`). |
| POST | `/api/v1/catalog/brands/{brandId}/approve` | Public | Approve; sets `isApproved=true` + `approvedBy`/`approvedAt`. |
| POST | `/api/v1/catalog/brands/{brandId}/reject` | Public | Reject with a `rejectionReason`; clears approval fields. |
| GET | `/api/v1/catalog/brands/{brandId}/audit-logs` | Public | List the approval audit trail for a brand. |

#### Example — Create a Catalog Product

```
POST /api/v1/catalog/products/
Content-Type: application/json

{
  "tenantId": "11111111-1111-1111-1111-111111111111",
  "storeId": "22222222-2222-2222-2222-222222222222",
  "name": "Classic Cotton Kurta",
  "slug": "classic-cotton-kurta",
  "description": "Handwoven cotton kurta with traditional block print detailing.",
  "status": "DRAFT",
  "productType": "PHYSICAL",
  "sku": "KUR-COT-001",
  "categoryId": "55555555-5555-5555-5555-555555555555",
  "brandId": "44444444-4444-4444-4444-444444444444",
  "shippingProfileId": "66666666-6666-6666-6666-666666666666"
}
```

```json
// 201 Created
{
  "id": "77777777-7777-7777-7777-777777777777",
  "tenantId": "11111111-1111-1111-1111-111111111111",
  "storeId": "22222222-2222-2222-2222-222222222222",
  "name": "Classic Cotton Kurta",
  "slug": "classic-cotton-kurta",
  "status": "DRAFT",
  "productType": "PHYSICAL",
  "sku": "KUR-COT-001",
  "categoryId": "55555555-5555-5555-5555-555555555555",
  "brandId": "44444444-4444-4444-4444-444444444444",
  "shippingProfileId": "66666666-6666-6666-6666-666666666666",
  "createdAt": "2026-08-28T10:20:00Z",
  "updatedAt": "2026-08-28T10:20:00Z",
  "deletedAt": null,
  "variants": [],
  "images": [],
  "attributeMappings": []
}
```

```json
// 403 Forbidden — Free-plan product cap reached (PlanLimitExceeded — structured `detail`, not a plain string)
{
  "detail": {
    "error": "plan_limit_exceeded",
    "message": "Your Free plan allows a maximum of 6 products. Please upgrade to add more.",
    "resource": "products",
    "limit": 6,
    "plan": "Free",
    "upgrade_required": true
  }
}
```

### Customers

> ⚠️ Every route in this section is **Public (no auth)** — including password-reset token issuance.

#### Customers — `/customers`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/customers/` | Public | Register a customer for a store; checks duplicate email/mobile per `storeId`; auto-generates `customerCode`; bcrypt-hashes `password` if provided. |
| GET | `/api/v1/customers/` | Public | Paginated list of non-deleted customers. Requires `storeId` query param or `X-Tenant-ID` header; filter by `status`, `isGuestCustomer`. |
| GET | `/api/v1/customers/{customer_id}` | Public | Fetch a single customer. |
| PATCH | `/api/v1/customers/{customer_id}` | Public | Partial profile update. |
| DELETE | `/api/v1/customers/{customer_id}` | Public | Soft-delete (`204`). |
| GET | `/api/v1/customers/{customer_id}/full` | Public | Same as get-by-id today (docstring implies address eager-loading that isn't implemented yet). |
| GET | `/api/v1/customers/trash/list` | Public | List soft-deleted customers. |
| POST | `/api/v1/customers/{customer_id}/restore` | Public | Restore a soft-deleted customer. |

#### Customer Addresses — `/addresses`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/addresses/` | Public | Create an address; unsets other `isDefault` addresses of the same type if `isDefault=true`. |
| GET | `/api/v1/addresses/customer/{customer_id}` | Public | List addresses for a customer. |
| GET | `/api/v1/addresses/{address_id}` | Public | Fetch a single address. |
| PATCH | `/api/v1/addresses/{address_id}` | Public | Partial update; re-applies the one-default-per-type rule. |
| DELETE | `/api/v1/addresses/{address_id}` | Public | Hard delete (`204`). |

#### Customer Sessions — `/sessions`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/sessions/` | Public | Create a session record (refresh token hash, IP, user agent, expiry). |
| GET | `/api/v1/sessions/customer/{customer_id}` | Public | List sessions; `active_only=true` filters to active. |
| GET | `/api/v1/sessions/{session_id}` | Public | Fetch a single session. |
| PATCH | `/api/v1/sessions/{session_id}` | Public | Update `logoutAt`/`isActive`. |
| DELETE | `/api/v1/sessions/{session_id}` | Public | Hard delete (invalidation, `204`). |

#### Guest Checkout — `/guest-checkouts`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/guest-checkouts/` | Public | Log a guest checkout (name/email/mobile, optional order/booking link). |
| GET | `/api/v1/guest-checkouts/` | Public | Paginated list, filter by `storeId`, `converted`. |
| GET | `/api/v1/guest-checkouts/{log_id}` | Public | Fetch a single log. |
| PATCH | `/api/v1/guest-checkouts/{log_id}` | Public | Update; auto-stamps `convertedAt` on first conversion. |
| DELETE | `/api/v1/guest-checkouts/{log_id}` | Public | Hard delete (`204`). |

#### Entity Verifications — `/verifications`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/verifications/` | Public | Create an OTP verification for a `CUSTOMER`/`ORDER`/`BOOKING` entity (`EMAIL`/`MOBILE`/`ORDER_CONFIRMATION`/`BOOKING_CONFIRMATION`). |
| GET | `/api/v1/verifications/` | Public | List, filter by `entityType`, `entityId`, `verificationType`. |
| GET | `/api/v1/verifications/{verification_id}` | Public | Fetch a single record. |
| PATCH | `/api/v1/verifications/{verification_id}` | Public | Update `verifiedAt`/`attempts` directly. |
| POST | `/api/v1/verifications/{verification_id}/verify` | Public | Mark verified; `409` if already verified, `410` if expired. |
| POST | `/api/v1/verifications/{verification_id}/increment-attempt` | Public | Increment the OTP attempt counter. |
| DELETE | `/api/v1/verifications/{verification_id}` | Public | Hard delete (`204`). |

#### Activity Logs — `/activity-logs`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/activity-logs/` | Public | Record a customer activity event (`LOGIN`, `ORDER_PLACED`, `WISHLIST_ADDED`, etc.). |
| GET | `/api/v1/activity-logs/customer/{customer_id}` | Public | Paginated history, filter by `activityType`. |
| GET | `/api/v1/activity-logs/{log_id}` | Public | Fetch a single entry. |

#### Customer Groups — `/groups`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/groups/` | Public | Create a customer segment/group. |
| GET | `/api/v1/groups/` | Public | List groups, optional `storeId`. |
| GET | `/api/v1/groups/{group_id}` | Public | Fetch a group. |
| PATCH | `/api/v1/groups/{group_id}` | Public | Update name/description. |
| DELETE | `/api/v1/groups/{group_id}` | Public | Delete (`204`). |
| POST | `/api/v1/groups/{group_id}/members` | Public | Add a customer; `409` if already a member. |
| GET | `/api/v1/groups/{group_id}/members` | Public | List members. |
| DELETE | `/api/v1/groups/{group_id}/members/{customer_id}` | Public | Remove a member; `404` if not a member. |

#### Customer Notes — `/notes`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/notes/` | Public | Create an internal note against a customer. |
| GET | `/api/v1/notes/customer/{customer_id}` | Public | List notes, newest first. |
| GET | `/api/v1/notes/{note_id}` | Public | Fetch a single note. |
| PATCH | `/api/v1/notes/{note_id}` | Public | Replace `noteText`. |
| DELETE | `/api/v1/notes/{note_id}` | Public | Delete (`204`). |

#### Customer Consents — `/consents`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/consents/` | Public | Log consent acceptance (`TERMS`, `PRIVACY_POLICY`, `EMAIL_MARKETING`, etc.). |
| GET | `/api/v1/consents/customer/{customer_id}` | Public | List consent history, optional `consentType`. |
| GET | `/api/v1/consents/{consent_id}` | Public | Fetch a single record. |

#### Password Reset (customers) — `/password-reset-tokens`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/password-reset-tokens/` | Public | Issue a reset token record (caller supplies pre-hashed `tokenHash`). |
| GET | `/api/v1/password-reset-tokens/customer/{customer_id}` | Public | List tokens for a customer. |
| PATCH | `/api/v1/password-reset-tokens/{token_id}/mark-used` | Public | Mark a token used; `409` if already used. |
| DELETE | `/api/v1/password-reset-tokens/{token_id}` | Public | Delete a token record (`204`). |

#### Example — Create a Customer

```
POST /api/v1/customers/
Content-Type: application/json

{
  "tenantId": "e2e56225-8da9-4414-9d71-d31f368d9ac7",
  "storeId": "d7bb739c-d79d-4ffd-8426-c0378e423f87",
  "firstName": "Anita",
  "lastName": "Sharma",
  "email": "anita.sharma@example.com",
  "mobile": "9876543210",
  "status": "ACTIVE",
  "isGuestCustomer": false,
  "password": "S3curePass!23"
}
```

```json
// 201 Created
{
  "id": "11111111-1111-1111-1111-111111111111",
  "tenantId": "e2e56225-8da9-4414-9d71-d31f368d9ac7",
  "storeId": "d7bb739c-d79d-4ffd-8426-c0378e423f87",
  "customerCode": "CUST-4F8A2C",
  "firstName": "Anita",
  "lastName": "Sharma",
  "email": "anita.sharma@example.com",
  "mobile": "9876543210",
  "status": "ACTIVE",
  "isGuestCustomer": false,
  "isEmailVerified": false,
  "isMobileVerified": false,
  "lastLoginAt": null,
  "createdAt": "2026-08-28T10:15:00Z",
  "updatedAt": "2026-08-28T10:15:00Z",
  "deletedAt": null
}
```

```json
// 409 Conflict (plain `{"detail": ...}` shape — this router raises HTTPException directly, not a service exception)
{ "detail": "Email already registered for this store" }
```

### Stores & Website Builder

> ⚠️ Only `stores.py` and `sections.py` enforce any authentication in this entire section — every other router (social links/platforms, bank accounts, themes, settings, deployments, publish logs, AI content, media, AI generation, domain verification, websites, admin websites) is fully public, including store bank-account CRUD. See [Known Issues & Caveats](#known-issues--caveats).

#### Stores — `/stores`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/stores/` | Bearer (role: platform_owner, store_owner) | Create a storefront; `409` if `storeSlug` taken. |
| GET | `/api/v1/stores/{storeId}` | Public | Fetch a store by UUID. |
| GET | `/api/v1/stores/slug/{storeSlug}` | Public | Fetch a store by URL slug. |
| GET | `/api/v1/stores/` | Bearer (any authenticated user) | List stores. Non-platform roles are silently scoped to their own `tenantId`. |
| PATCH | `/api/v1/stores/{storeId}` | Bearer (role: platform_owner, store_owner, store_admin) | Update store fields; `409` on slug collision. |
| DELETE | `/api/v1/stores/{storeId}` | Bearer (role: platform_owner) | Delete a store. |
| POST | `/api/v1/stores/{storeId}/submit` | Public | ⚠️ **Broken** — `StoreService.submitForApproval` is accidentally nested inside `deleteStore()` in the source, so every call raises `AttributeError` → 500. See [Known Issues](#known-issues--caveats). |
| POST | `/api/v1/stores/{storeId}/publish` | Public | Publish an approved store; `409` if not `APPROVED`. |
| GET | `/api/v1/stores/{storeId}/preview` | Public | Return a preview-URL payload. |
| PATCH | `/api/v1/stores/{storeId}/theme` | Public | Change theme. **Note:** `themeId` is a query parameter, not a path/body field. |
| POST | `/api/v1/stores/{storeId}/generate-ai` | Public | ⚠️ **Broken** — `StoreService.generateAI` does not exist; every call raises `AttributeError` → 500. |
| POST | `/api/v1/stores/{storeId}/connect-domain` | Public | Stub — `domain` query param, echoes back without persisting. |
| GET | `/api/v1/stores/{storeId}/status` | Public | Returns `{storeId, status, isActive}`. |

#### Sections — `/sections`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/sections/` | Bearer (role: platform_owner, store_owner, store_admin) | Create a page section block. |
| GET | `/api/v1/sections/{sectionId}` | Public | Fetch a section. |
| GET | `/api/v1/sections/` | Public | List sections for a store (`storeId` required). |
| PATCH | `/api/v1/sections/{sectionId}` | Bearer (role: platform_owner, store_owner, store_admin) | Update a section's config. |
| DELETE | `/api/v1/sections/{sectionId}` | Bearer (role: platform_owner, store_owner) | Delete (`204`). |

#### Social Links — `/social-links`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/social-links/` | Public | Link a store to a platform handle/URL; `409` if one exists for that platform+store. |
| GET | `/api/v1/social-links/{socialLinkId}` | Public | Fetch a link. |
| GET | `/api/v1/social-links/` | Public | List, optional `storeId`. |
| PATCH | `/api/v1/social-links/{socialLinkId}` | Public | Update URL/active state. |
| DELETE | `/api/v1/social-links/{socialLinkId}` | Public | Delete (`204`). |

#### Social Platforms — `/social-platforms`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/social-platforms/` | Public | Register a platform master row; `409` on duplicate `platformCode`. |
| GET | `/api/v1/social-platforms/{platformId}` | Public | Fetch a platform. |
| GET | `/api/v1/social-platforms/` | Public | List; `activeOnly=true` filters. |
| PATCH | `/api/v1/social-platforms/{platformId}` | Public | Update properties. |
| DELETE | `/api/v1/social-platforms/{platformId}` | Public | Delete (`204`). |

#### Store Bank Accounts — `/store-bank-accounts`
⚠️ Sensitive data, zero auth/ownership checks.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/store-bank-accounts/` | Public | Register a payout bank account. |
| GET | `/api/v1/store-bank-accounts/{bankAccountId}` | Public | Fetch by ID. |
| GET | `/api/v1/store-bank-accounts/` | Public | List, optional `storeId`. |
| PATCH | `/api/v1/store-bank-accounts/{bankAccountId}` | Public | Update details (e.g. toggle primary payout). |
| DELETE | `/api/v1/store-bank-accounts/{bankAccountId}` | Public | Delete (`204`). |

#### Website Themes — `/website-themes`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/website-themes/` | Public | Register a theme template; `409` on duplicate `themeCode`. |
| GET | `/api/v1/website-themes/{themeId}` | Public | Fetch a theme. |
| GET | `/api/v1/website-themes/` | Public | List; `activeOnly=true` filters. |
| PATCH | `/api/v1/website-themes/{themeId}` | Public | Update a theme. |
| DELETE | `/api/v1/website-themes/{themeId}` | Public | Delete (`204`). |

#### Website Settings — `/website-settings`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/website-settings/` | Public | Create settings for a store; `409` if they already exist. |
| GET | `/api/v1/website-settings/store/{storeId}` | Public | Fetch by store ID; `404` if none. |
| PATCH | `/api/v1/website-settings/store/{storeId}` | Public | Update settings. |

#### Website Deployments — `/website-deployments`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/website-deployments/` | Public | Create a deployment record; `400` if `provider` is blank. |
| GET | `/api/v1/website-deployments/{deploymentId}` | Public | Fetch by ID. |
| GET | `/api/v1/website-deployments/store/{storeId}` | Public | List for a store. |
| POST | `/api/v1/website-deployments/{deploymentId}/start` | Public | Transition to "started"; `409` if not startable. |
| POST | `/api/v1/website-deployments/{deploymentId}/success` | Public | Mark success. `deploymentUrl` is a query parameter. |
| POST | `/api/v1/website-deployments/{deploymentId}/failed` | Public | Mark failure. `errorMessage` is a query parameter. |
| PATCH | `/api/v1/website-deployments/{deploymentId}/status` | Public | Generic status update via required `deploymentStatus` query parameter. |

#### Website Publish Logs — `/website-publish-logs`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/website-publish-logs/` | Public | Create a publish-log entry. |
| GET | `/api/v1/website-publish-logs/{logId}` | Public | Fetch a single log. |
| GET | `/api/v1/website-publish-logs/store/{storeId}` | Public | List for a store. |

#### Website AI Content — `/website-ai-content`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/website-ai-content/` | Public | Create an AI-generated content record. |
| GET | `/api/v1/website-ai-content/{contentId}` | Public | Fetch a record. |
| GET | `/api/v1/website-ai-content/store/{storeId}` | Public | List for a store. |
| PATCH | `/api/v1/website-ai-content/{contentId}` | Public | Update (e.g. after manual edit/approval). |

#### Website Media — `/website-media`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/website-media/` | Public | Create the media set (logo/banner/gallery); `409` if one exists for the `websiteId`. |
| GET | `/api/v1/website-media/website/{websiteId}` | Public | Fetch by website ID; `404` if none. |
| PATCH | `/api/v1/website-media/website/{websiteId}` | Public | Partial update. |

#### Website AI Generation — `/website-ai`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/website-ai/generate` | Public | Calls Gemini to generate website content; `400` on invalid `contentType`, `502`-style error on provider failure/missing key. |

#### Domain Verification — `/domains/{domainId}`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/domains/{domainId}/verification-token` | Public | Generate a DNS verification token for a custom domain. |
| POST | `/api/v1/domains/{domainId}/verify` | Public | Verify DNS ownership via `verificationToken` query parameter; `409` on mismatch. |

#### Websites — `/websites`
The "company website" builder entity — distinct from `stores.py`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/websites/create` | Public | Create a website/site record for a tenant. |
| PUT | `/api/v1/websites/update` | Public | Update a website. **Note:** `websiteId` is a query parameter, not path. |
| GET | `/api/v1/websites/{websiteId}` | Public | Fetch by ID. |
| POST | `/api/v1/websites/submit` | Public | Submit (`websiteId` in body) for admin approval. |
| GET | `/api/v1/websites/preview/{slug}` | Public | Preview payload by slug. |

#### Admin Websites — `/admin/websites`
Despite the `/admin` path, no auth is enforced.

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/admin/websites/pending` | Public | List websites awaiting approval. |
| GET | `/api/v1/admin/websites/{websiteId}` | Public | Fetch a website (admin view). |
| POST | `/api/v1/admin/websites/approve` | Public | Approve a website (`websiteId` + optional `reason`). |
| POST | `/api/v1/admin/websites/reject` | Public | Reject a website. |
| POST | `/api/v1/admin/websites/publish` | Public | Publish an approved website. |

#### Public Website — `publicWebsite.py` (declares no router prefix)

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/company/{slug}` | Public | Public storefront lookup by slug; `404` unless `status == "LIVE"`. |
| GET | `/api/v1/` | Public | Resolves a website by the `Host` header for custom-domain routing; `404` if no `LIVE` match. Lands on the bare API root since this router adds no prefix. |

#### Example — Create a Store

```
POST /api/v1/stores/
Authorization: Bearer <store-owner-token>
Content-Type: application/json

{
  "tenantId": "e2e56225-8da9-4414-9d71-d31f368d9ac7",
  "storeName": "Jack's Boutique",
  "storeSlug": "jacks-boutique",
  "tagline": "Handcrafted fashion, delivered fast",
  "email": "hello@jacksboutique.com",
  "mobile": "9123456780",
  "isActive": true,
  "approvalStatus": "DRAFT"
}
```

```json
// 201 Created
{
  "id": "66666666-6666-6666-6666-666666666666",
  "tenantId": "e2e56225-8da9-4414-9d71-d31f368d9ac7",
  "storeName": "Jack's Boutique",
  "storeSlug": "jacks-boutique",
  "email": "hello@jacksboutique.com",
  "mobile": "9123456780",
  "isActive": true,
  "approvalStatus": "DRAFT",
  "createdAt": "2026-08-28T10:20:00Z",
  "updatedAt": "2026-08-28T10:20:00Z"
}
```

```json
// 409 Conflict (structured envelope — StoreService raises ConflictError)
{ "error": { "code": "CONFLICT", "message": "Store with slug 'jacks-boutique' already exists" } }
```

### Approvals, Auditing & Versioning

> ⚠️ Only `auditLogs.py` enforces any authentication in this section — `approvalRequests.py`, `entityVersions.py`, `statusHistory.py`, and `reviewQueue.py` are entirely public, including destructive/approval-granting actions. All routers here re-catch `NotFoundError`/`BusinessValidationError`/`ConflictError` and re-raise as plain `HTTPException`, so responses use `{"detail": "..."}` even though those exception classes could otherwise auto-envelope.

#### Approval Requests — `/approval-requests`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/approval-requests/draft` | Public | Save entity changes as an unpublished draft `EntityVersion` (no submission). |
| POST | `/api/v1/approval-requests/submit` | Public | Submit a change request for review; creates a version snapshot and seeds the Review Queue. |
| PUT | `/api/v1/approval-requests/{requestId}/draft` | Public | Modify the `versionData` of a still-`PENDING` request. |
| POST | `/api/v1/approval-requests/{requestId}/withdraw` | Public | Withdraw a `PENDING` request. |
| POST | `/api/v1/approval-requests/{requestId}/approve` | Public | Approve; applies the version data to the live entity. |
| POST | `/api/v1/approval-requests/{requestId}/reject` | Public | Reject with a mandatory `rejectionReason`. |
| GET | `/api/v1/approval-requests/` | Public | List, filter by `tenantId`, `entityType`, `entityId`, `approvalStatus`. |
| GET | `/api/v1/approval-requests/{requestId}` | Public | Get by ID. |
| DELETE | `/api/v1/approval-requests/{requestId}` | Public | Hard-delete (admin utility route). |

#### Entity Versions — `/entity-versions`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/entity-versions/` | Public | Manually create a version snapshot row. |
| GET | `/api/v1/entity-versions/` | Public | List, filter by `tenantId`, `entityType`, `entityId`, `isPublished`. |
| GET | `/api/v1/entity-versions/preview` | Public | Latest unpublished (draft) version for an entity, falling back to latest overall. |
| GET | `/api/v1/entity-versions/{versionId}` | Public | Get a single version snapshot. |
| POST | `/api/v1/entity-versions/{versionId}/rollback` | Public | Restore the live entity to a historical snapshot; creates a `RESTORE` audit entry. |

#### Audit Logs — `/audit-logs`
The only authenticated router in this section.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/audit-logs/` | Bearer (role: platform_owner) | Create an audit log entry. |
| GET | `/api/v1/audit-logs/` | Bearer (role: platform_owner, platform_staff) | List, filter by `tenantId`, `entityType`, `entityId`, `actionType`, `performedBy`. |
| GET | `/api/v1/audit-logs/{logId}` | Bearer (role: platform_owner, platform_staff) | Get a single entry. |

#### Status History — `/status-history`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/status-history/` | Public | Create a status-transition record. |
| GET | `/api/v1/status-history/` | Public | List, filter by `tenantId`, `entityType`, `entityId`, `newStatus`, `changedBy`. |
| GET | `/api/v1/status-history/{historyId}` | Public | Get a single record. |
| DELETE | `/api/v1/status-history/{historyId}` | Public | Hard-delete. |

#### Review Queue — `/review-queue`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/review-queue/` | Public | List, filter by `tenantId`, `entityType`, `approvalStatus`, `assignedTo`; sortable. |
| GET | `/api/v1/review-queue/{queueId}` | Public | Get a single item. |
| PATCH | `/api/v1/review-queue/{queueId}/assign` | Public | Reassign `assignedTo`. |
| POST | `/api/v1/review-queue/bulk-action` | Public | Bulk `APPROVE`/`REJECT` a list of `requestIds` — **never returns an HTTP error**; per-item failures are reported inline as `200 OK` with `{"processed": N, "details": [{"requestId", "status": "FAILED", "error": "..."}]}`. |

### Live Chat

A **completely separate auth system** from the main platform: its own `ChatUser` table, its own JWT issuance in `app/core/securityChat.py`, its own `/chat-auth/login`. The resulting "Chat JWT" is not interchangeable with the platform's access token, even though both may be signed with the same `jwtSecretKey`.

#### Chat Authentication — `/chat-auth`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/chat-auth/register` | Public | Register a chat user (`customer`/`store_owner`/`support_agent`) and immediately log in, returning a Chat JWT. |
| POST | `/api/v1/chat-auth/login` | Public | Authenticate by email/password; issues a Chat JWT. |
| GET | `/api/v1/chat-auth/users/lookup` | Public | Look up a chat user's id/name/role by email. |
| GET | `/api/v1/chat-auth/stores/lookup` | Public | Look up the `store_owner` ChatUser that owns a given `storeId`. |

`POST /login` failures raise `AuthenticationError`/`AccountLockedError` (both `AppException` subclasses) → auto-enveloped `{"error": {"code": "UNAUTHORIZED", "message": "..."}}`, `401`. The two lookup routes never error on a miss — they return `200 OK` with `{"found": false}`.

#### Live Chat WebSocket

| Method | Path | Auth | Description |
|---|---|---|---|
| WS | `/api/v1/ws/chat/{userId}` | Chat JWT via `?token=` query param, decoded by hand (not FastAPI dependency injection) | Bidirectional chat socket between customers, store owners, and support agents. |
| GET | `/api/v1/chat-test` | Public | Liveness check — `{"message": "Chat router working"}`. |

**Connect:** `ws://<host>/api/v1/ws/chat/{userId}?token=<chat_access_token>` — `{userId}` must match the token's `sub` claim, else the server closes with code `4001` (also used for an invalid/expired token). No HTTP 401 is ever produced for a bad token — only a socket close or, once connected, in-band `{"event": "error", "detail": "..."}` frames.

Client → server (over the open socket):
```json
{
  "event": "message",
  "chatType": "customer_owner",
  "storeId": 42,
  "receiverId": null,
  "message": "Hi, is this product in stock?"
}
```
`chatType` is `"customer_owner"` or `"owner_support"`; a `customer` sender supplies `storeId` (server resolves the owner), a `store_owner`/`support_agent` sender supplies `receiverId` directly.

Server → sender acknowledgement:
```json
{ "event": "message_sent", "messageId": 501, "conversationId": 77, "storeId": 42 }
```

Server → recipient push:
```json
{ "event": "message", "conversationId": 77, "storeId": 42, "messageId": 501, "senderId": 12, "message": "Hi, is this product in stock?" }
```

#### Example — Chat Login

```
POST /api/v1/chat-auth/login
Content-Type: application/json

{ "email": "priya.owner@example.com", "password": "StrongPass!123" }
```

```json
// 200 OK
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "bearer",
  "userId": 12,
  "role": "store_owner",
  "storeId": 42
}
```

This `accessToken` is used as the WebSocket `token` query parameter, not as an `Authorization` header:
```
ws://localhost:8000/api/v1/ws/chat/12?token=eyJhbGciOiJIUzI1NiIs...
```

```json
// 401 Unauthorized (structured envelope — AuthenticationError is an AppException)
{ "error": { "code": "UNAUTHORIZED", "message": "Invalid email or password" } }
```

### Invoice Generator

#### Invoice — `/invoice`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/invoice/generate` | Public | Render a GST-style tax invoice PDF from company/party/line-item data. Returns a binary PDF, not JSON. |

**Response:** `application/pdf` byte stream, `Content-Disposition: attachment; filename=invoice_<number>.pdf`.

#### Example — Generate an Invoice

```
POST /api/v1/invoice/generate
Content-Type: application/json

{
  "company": { "gstin": "27AADCK1234A1Z5", "name": "KAROBARONE PVT. LTD.", "address1": "Sector-5, Salt Lake, Kolkata - 700091", "state": "West Bengal" },
  "bill_to": { "name": "Rohan Traders", "address": "12 MG Road, Bengaluru - 560001", "state": "Karnataka - 29", "gstin": "29AAACR5055K1Z5" },
  "ship_to": { "name": "Rohan Traders - Warehouse", "address": "Plot 7, Whitefield Industrial Area, Bengaluru - 560066", "state": "Karnataka - 29", "gstin": "29AAACR5055K1Z5" },
  "invoice": { "number": "INV-2026-0091", "date": "2026-08-28", "payment_mode": "UPI", "reverse_charge": "NO" },
  "items": [
    { "sr": 1, "description": "Wireless Barcode Scanner - Model BX200", "hsn": "8471", "qty": 10, "unit": "Nos", "rate": 2500.0, "gst_pct": 18 }
  ]
}
```

```
// 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename=invoice_INV-2026-0091.pdf

%PDF-1.4 ... (binary PDF bytes) ...
```

```json
// 422 Unprocessable Entity — invalid GSTIN format (Pydantic field_validator)
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "type": "value_error", "loc": ["body", "bill_to", "gstin"], "msg": "Value error, Invalid GSTIN format: '29AAACR5055K1Z'" }
    ]
  }
}
```

```json
// 500 — PDF rendering failure (plain shape)
{ "detail": "Failed to generate invoice: [Errno 2] No such file or directory: '...'" }
```

### AI Blog Agent

#### Blog Writer AI Agent — `/blog-agent`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/blog-agent/generate` | Public (plan-gated only if `tenantId` is supplied) | Runs the LangGraph blog-writing agent for a `topic`; returns a plan + markdown + image specs. |

If `tenantId` is supplied, `PlanGuard.check_feature_access(tenantId, "blog")` runs first and can reject with a structured `{"error": {"code": ..., "message": "..."}}` if the tenant's plan doesn't include the `blog` feature. If `tenantId` is omitted, the agent always runs with no entitlement check. Agent failures return `500 {"detail": "AI Agent run failed: ..."}`.

### Commerce Suite (`/github`): Carts, Orders & Payments

This whole module lives under `app/api/v1/endpoints/github/`, mounted at `/api/v1/github<router-prefix><route>`. It ships its own `authRouter.py` (`/github/auth/register`, `/github/auth/login`), but `authService.login()` only verifies a bcrypt hash and returns the raw user row — **no JWT is ever issued or checked**. Every route below uses only `Depends(getSyncDb)`.

> ⚠️ **Every single endpoint in this subsection is Public (no auth).** This is a significant gap for a commerce API handling carts/orders/payments/payouts — see [Known Issues & Caveats](#known-issues--caveats). Unhandled `IntegrityError`s (duplicate/FK violations) are caught globally and returned as `409 {"error": {"code": "CONFLICT", "message": "Database constraint violation..."}}`; explicit not-found checks use the plain `{"detail": "..."}` shape.

#### Cart — `/cart`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/cart/` | Create a cart |
| GET | `/api/v1/github/cart/` | List all carts |
| GET | `/api/v1/github/cart/{cartId}` | Get a cart |
| PUT | `/api/v1/github/cart/{cartId}` | Update a cart |
| DELETE | `/api/v1/github/cart/{cartId}` | Delete a cart |

#### Cart Items — `/cart-items`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/cart-items/` | Add an item to a cart |
| GET | `/api/v1/github/cart-items/by-cart/{cartId}` | List items in a cart |
| GET | `/api/v1/github/cart-items/{cartItemId}` | Get a cart item |
| PUT | `/api/v1/github/cart-items/{cartItemId}` | Update a cart item (e.g. quantity) |
| DELETE | `/api/v1/github/cart-items/{cartItemId}` | Remove an item |

#### Cart Coupons — `/cart-coupons`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/cart-coupons/` | Attach a coupon to a cart |
| GET | `/api/v1/github/cart-coupons/` | List cart-coupon records |
| GET | `/api/v1/github/cart-coupons/{couponId}` | Get a record |
| PUT | `/api/v1/github/cart-coupons/{couponId}` | Update a record |
| DELETE | `/api/v1/github/cart-coupons/{couponId}` | Remove a coupon from a cart |

#### Abandoned Carts — `/abandoned-carts`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/abandoned-carts/` | Record an abandoned cart |
| GET | `/api/v1/github/abandoned-carts/` | List records |
| GET | `/api/v1/github/abandoned-carts/{abandonedCartId}` | Get a record |
| PUT | `/api/v1/github/abandoned-carts/{abandonedCartId}` | Update (e.g. recovery status) |
| DELETE | `/api/v1/github/abandoned-carts/{abandonedCartId}` | Delete a record |

#### Checkout — `/checkout`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/checkout` | Compute a checkout summary (subtotal/discount/shipping/tax/total) from the active cart. ⚠️ **Does not create an Order** — per the source's own "Phase 1" comment, it only reads stored cart totals. Order creation is `POST /orders/` below. |

#### Orders — `/orders`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/orders/` | **Create (persist) an order** — the real order-creation endpoint (worked example below) |
| GET | `/api/v1/github/orders/` | List all orders |
| GET | `/api/v1/github/orders/{orderId}` | Get an order (`404` if missing) |
| PUT | `/api/v1/github/orders/{orderId}` | Update status/fulfillment/note fields |
| DELETE | `/api/v1/github/orders/{orderId}` | Delete an order |

#### Order Items — `/order-items`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/order-items/` | Create an order line item |
| GET | `/api/v1/github/order-items/` | List all order items |
| GET | `/api/v1/github/order-items/{orderItemId}` | Get an item |
| PUT | `/api/v1/github/order-items/{orderItemId}` | Update an item |
| DELETE | `/api/v1/github/order-items/{orderItemId}` | Delete an item |

#### Order Status — `/order-status`
| Method | Path | Description |
|---|---|---|
| PUT | `/api/v1/github/order-status` | Status-transition engine — updates `order_status`/`payment_status`/`fulfillment_status` for an `order_id` in one call |

#### Order Cancellations — `/order-cancellations`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/order-cancellations/` | Create a cancellation record |
| GET | `/api/v1/github/order-cancellations/{orderCancellationId}` | Get by its own ID |
| GET | `/api/v1/github/order-cancellations/by-order/{orderId}` | Get by order ID |
| PUT | `/api/v1/github/order-cancellations/{orderCancellationId}` | Update |
| DELETE | `/api/v1/github/order-cancellations/{orderCancellationId}` | Delete |

#### Order Returns — `/order-returns`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/order-returns/` | Create a return record |
| GET | `/api/v1/github/order-returns/{orderReturnId}` | Get by its own ID |
| GET | `/api/v1/github/order-returns/by-order/{orderId}` | Get by order ID |
| PUT | `/api/v1/github/order-returns/{orderReturnId}` | Update |
| DELETE | `/api/v1/github/order-returns/{orderReturnId}` | Delete |

#### Order Refunds — `/order-refunds`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/order-refunds/` | Create an order-level refund |
| GET | `/api/v1/github/order-refunds/` | List, filter by `orderId`/`refundStatus` |
| GET | `/api/v1/github/order-refunds/{orderRefundId}` | Get by ID |
| GET | `/api/v1/github/order-refunds/by-order/{orderId}` | List for an order |
| PUT | `/api/v1/github/order-refunds/{orderRefundId}` | Update |
| DELETE | `/api/v1/github/order-refunds/{orderRefundId}` | Delete |

#### Payments — `/payments`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/payments/` | Create a plain payment record — no gateway call (worked example below) |
| GET | `/api/v1/github/payments/` | List all payments |
| GET | `/api/v1/github/payments/{paymentId}` | Get a payment (`404` if missing) |
| POST | `/api/v1/github/payments/create-order` | Create a Razorpay order via the gateway (no DB write) |
| POST | `/api/v1/github/payments/verify` | Verify a Razorpay payment signature |
| POST | `/api/v1/github/payments/refund` | Refund a payment via Razorpay |
| POST | `/api/v1/github/payments/create-payment-order` | Combined flow: persists a `Payment` row, then creates the matching Razorpay order |

#### Payment Methods — `/payment-methods`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/payment-methods/` | Create a payment method |
| GET | `/api/v1/github/payment-methods/` | List all |
| GET | `/api/v1/github/payment-methods/{paymentMethodId}` | Get one |
| PUT | `/api/v1/github/payment-methods/{paymentMethodId}` | Update |
| DELETE | `/api/v1/github/payment-methods/{paymentMethodId}` | Delete |

#### Payment Refunds — `/payment-refunds`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/payment-refunds/` | Create a payment-level refund |
| GET | `/api/v1/github/payment-refunds/` | List all |
| GET | `/api/v1/github/payment-refunds/{refundId}` | Get one |
| PUT | `/api/v1/github/payment-refunds/{refundId}` | Update |
| DELETE | `/api/v1/github/payment-refunds/{refundId}` | Delete |

#### Payment Audit Logs — `/payment-audit-logs`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/payment-audit-logs/` | Create an entry |
| GET | `/api/v1/github/payment-audit-logs/` | List all |
| GET | `/api/v1/github/payment-audit-logs/{auditId}` | Get one |
| PUT | `/api/v1/github/payment-audit-logs/{auditId}` | Update |
| DELETE | `/api/v1/github/payment-audit-logs/{auditId}` | Delete |

#### Subscription Payments — `/subscription-payments`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/subscription-payments/` | Create a record |
| GET | `/api/v1/github/subscription-payments/` | List all |
| GET | `/api/v1/github/subscription-payments/{paymentId}` | Get one |
| PUT | `/api/v1/github/subscription-payments/{paymentId}` | Update |
| DELETE | `/api/v1/github/subscription-payments/{paymentId}` | Delete |

#### Gateway Settlements — `/gateway-settlements`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/gateway-settlements/` | Create a settlement batch |
| GET | `/api/v1/github/gateway-settlements/` | List all |
| GET | `/api/v1/github/gateway-settlements/{settlementId}` | Get one |
| PUT | `/api/v1/github/gateway-settlements/{settlementId}` | Update |
| DELETE | `/api/v1/github/gateway-settlements/{settlementId}` | Delete |

#### Gateway Settlement Items — `/gateway-settlement-items`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/gateway-settlement-items/` | Create a line item |
| GET | `/api/v1/github/gateway-settlement-items/` | List all |
| GET | `/api/v1/github/gateway-settlement-items/{itemId}` | Get one |
| PUT | `/api/v1/github/gateway-settlement-items/{itemId}` | Update |
| DELETE | `/api/v1/github/gateway-settlement-items/{itemId}` | Delete |

#### Gateway Webhook Events — `/gateway-webhook-events`
No DELETE route — audit-trail style (create/read/update only).

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/gateway-webhook-events/` | Record an inbound webhook event |
| GET | `/api/v1/github/gateway-webhook-events/` | List all |
| GET | `/api/v1/github/gateway-webhook-events/{eventId}` | Get one |
| PUT | `/api/v1/github/gateway-webhook-events/{eventId}` | Update (e.g. mark processed) |

#### Payment Reconciliation Batches — `/payment-reconciliation-batches`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/payment-reconciliation-batches/` | Create a batch |
| GET | `/api/v1/github/payment-reconciliation-batches/` | List all |
| GET | `/api/v1/github/payment-reconciliation-batches/{batchId}` | Get one |
| PUT | `/api/v1/github/payment-reconciliation-batches/{batchId}` | Update |
| DELETE | `/api/v1/github/payment-reconciliation-batches/{batchId}` | Delete |

#### Payment Reconciliation Items — `/payment-reconciliation-items`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/payment-reconciliation-items/` | Create a reconciliation-item row |
| GET | `/api/v1/github/payment-reconciliation-items/` | List all |
| GET | `/api/v1/github/payment-reconciliation-items/{itemId}` | Get one |
| PUT | `/api/v1/github/payment-reconciliation-items/{itemId}` | Update |
| DELETE | `/api/v1/github/payment-reconciliation-items/{itemId}` | Delete |

#### Revenue Summary — `/revenue-summary`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/revenue-summary/` | Create a revenue-summary record |
| GET | `/api/v1/github/revenue-summary/` | List all |
| GET | `/api/v1/github/revenue-summary/{revenueId}` | Get one |
| PUT | `/api/v1/github/revenue-summary/{revenueId}` | Update |
| DELETE | `/api/v1/github/revenue-summary/{revenueId}` | Delete |

#### Commission — `/commission`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/commission/calculate` | Stateless: given `order_id`/`order_amount`/`commission_percentage`, returns `commission_amount` + `seller_amount` (rounded half-up). Does not persist anything. |

#### Seller Payouts — `/seller-payouts`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/seller-payouts/` | Create a payout record |
| GET | `/api/v1/github/seller-payouts/` | List all |
| GET | `/api/v1/github/seller-payouts/{payoutId}` | Get one |
| PUT | `/api/v1/github/seller-payouts/{payoutId}` | Update (e.g. mark paid) |
| DELETE | `/api/v1/github/seller-payouts/{payoutId}` | Delete |

#### Example — Create an Order

A realistic flow: call checkout for totals, then create the order with those totals.

```
POST /api/v1/github/checkout
Content-Type: application/json

{ "customer_id": "22222222-2222-2222-2222-222222222222", "shipping_address_id": "33333333-3333-3333-3333-333333333333", "coupon_code": "WELCOME10" }
```
```json
// 200 OK
{ "cart_id": "11111111-1111-1111-1111-111111111111", "total_items": 3, "subtotal": 1699.00, "discount": 200.00, "shipping": 0.00, "tax": 76.46, "grand_total": 1575.46, "currency": "INR" }
```

```
POST /api/v1/github/orders/
Content-Type: application/json

{
  "tenant_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "store_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
  "customer_id": "22222222-2222-2222-2222-222222222222",
  "cart_id": "11111111-1111-1111-1111-111111111111",
  "order_number": "ORD-2026-000482",
  "billing_address_id": "44444444-4444-4444-4444-444444444444",
  "shipping_address_id": "33333333-3333-3333-3333-333333333333",
  "order_status": "PENDING",
  "payment_status": "PENDING",
  "fulfillment_status": "PENDING",
  "subtotal_amount": 1699.00,
  "discount_amount": 200.00,
  "tax_amount": 76.46,
  "shipping_amount": 0.00,
  "total_amount": 1575.46,
  "currency_code": "INR"
}
```

```json
// 201 Created
{
  "id": "55555555-5555-5555-5555-555555555555",
  "tenant_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "store_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
  "customer_id": "22222222-2222-2222-2222-222222222222",
  "cart_id": "11111111-1111-1111-1111-111111111111",
  "order_number": "ORD-2026-000482",
  "order_status": "PENDING",
  "payment_status": "PENDING",
  "fulfillment_status": "PENDING",
  "total_amount": 1575.46,
  "currency_code": "INR",
  "placed_at": "2026-08-28T10:15:00Z",
  "created_at": "2026-08-28T10:15:00Z",
  "updated_at": "2026-08-28T10:15:00Z"
}
```

```json
// 409 Conflict — duplicate order_number or an FK violation (global IntegrityError handler)
{ "error": { "code": "CONFLICT", "message": "Database constraint violation. A related record may not exist or a duplicate exists." } }
```

```json
// 404 Not Found — GET /orders/{orderId} with an unknown id (plain shape)
{ "detail": "Order not found." }
```

#### Example — Create a Payment

```
POST /api/v1/github/payments/
Content-Type: application/json

{
  "tenant_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "store_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
  "entity_type": "ORDER",
  "entity_id": "55555555-5555-5555-5555-555555555555",
  "payment_method_id": "66666666-6666-6666-6666-666666666666",
  "amount": 1575.46,
  "currency": "INR"
}
```

```json
// 200 OK (no response_model on this route — raw ORM object)
{
  "id": "77777777-7777-7777-7777-777777777777",
  "tenant_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "entity_type": "ORDER",
  "entity_id": "55555555-5555-5555-5555-555555555555",
  "amount": 1575.46,
  "currency": "INR",
  "payment_status": "PENDING",
  "payment_date": null,
  "created_at": "2026-08-28T10:16:00Z"
}
```

```json
// 409 Conflict — payment_method_id points at a nonexistent row (FK violation)
{ "error": { "code": "CONFLICT", "message": "Database constraint violation. A related record may not exist or a duplicate exists." } }
```

```json
// 422 Unprocessable Entity — missing "amount"
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [ { "type": "missing", "loc": ["body", "amount"], "msg": "Field required" } ]
  }
}
```

### Commerce Suite (`/github`): Shipping, Bookings, Offers & Wishlist

Same module, same mounting rule (`/api/v1/github<router-prefix><route>`). **Every endpoint below is also Public (no auth)** — none of these 32 files use any auth dependency, and none use the platform's `NotFoundError`/`ConflictError` exception classes either: every error here is a plain `fastapi.HTTPException` → `{"detail": "..."}` (validation errors still go through the global `{"error": {"code": "VALIDATION_ERROR", ...}}` handler).

#### Shipping Profiles — `/shipping-profiles`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipping-profiles/` | Create a shipping profile |
| GET | `/api/v1/github/shipping-profiles/` | List all |
| GET | `/api/v1/github/shipping-profiles/{profileId}` | Get one |
| PUT | `/api/v1/github/shipping-profiles/{profileId}` | Update |
| DELETE | `/api/v1/github/shipping-profiles/{profileId}` | Delete |

#### Shipping Zones — `/shipping-zones`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipping-zones/` | Create a zone |
| GET | `/api/v1/github/shipping-zones/` | List all |
| GET | `/api/v1/github/shipping-zones/{zoneId}` | Get one |
| PUT | `/api/v1/github/shipping-zones/{zoneId}` | Update |
| DELETE | `/api/v1/github/shipping-zones/{zoneId}` | Delete |

#### Shipping Rates — `/shipping-rates`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipping-rates/` | Create a rate |
| GET | `/api/v1/github/shipping-rates/` | List all |
| GET | `/api/v1/github/shipping-rates/{rateId}` | Get one |
| PUT | `/api/v1/github/shipping-rates/{rateId}` | Update |
| DELETE | `/api/v1/github/shipping-rates/{rateId}` | Delete |

#### Shipping Profile Zones — `/shipping-profile-zones`
Create/read/delete only — no update route.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipping-profile-zones/` | Link a profile to a zone |
| GET | `/api/v1/github/shipping-profile-zones/` | List all links |
| GET | `/api/v1/github/shipping-profile-zones/{objId}` | Get one link |
| DELETE | `/api/v1/github/shipping-profile-zones/{objId}` | Remove a link |

#### Shipping Partners — `/shipping-partners`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipping-partners/` | Create a courier partner |
| GET | `/api/v1/github/shipping-partners/` | List all |
| GET | `/api/v1/github/shipping-partners/{partnerId}` | Get one |
| PUT | `/api/v1/github/shipping-partners/{partnerId}` | Update |
| DELETE | `/api/v1/github/shipping-partners/{partnerId}` | Delete |

#### Shipments — `/shipments`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipments/` | Create a shipment |
| GET | `/api/v1/github/shipments/` | List all |
| GET | `/api/v1/github/shipments/{shipmentId}` | Get one |
| PUT | `/api/v1/github/shipments/{shipmentId}` | Update |
| DELETE | `/api/v1/github/shipments/{shipmentId}` | Delete |

#### Shipment Requests — `/shipment-requests`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipment-requests/` | Create a shipment request |
| GET | `/api/v1/github/shipment-requests/` | List all |
| GET | `/api/v1/github/shipment-requests/{requestId}` | Get one |
| PUT | `/api/v1/github/shipment-requests/{requestId}` | Update |
| DELETE | `/api/v1/github/shipment-requests/{requestId}` | Delete |

#### Shipping Exceptions — `/shipping-exceptions`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shipping-exceptions/` | Record an exception (failed delivery, damage) |
| GET | `/api/v1/github/shipping-exceptions/` | List all |
| GET | `/api/v1/github/shipping-exceptions/{shippingExceptionId}` | Get one |
| PUT | `/api/v1/github/shipping-exceptions/{shippingExceptionId}` | Update |
| DELETE | `/api/v1/github/shipping-exceptions/{shippingExceptionId}` | Delete |

#### Shiprocket — `/shiprocket`
A thin proxy over the third-party Shiprocket courier API — no local persistence.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/shiprocket/login` | Authenticate with Shiprocket, obtain their API token |
| POST | `/api/v1/github/shiprocket/order` | Create an order in Shiprocket |
| GET | `/api/v1/github/shiprocket/serviceability` | Check pincode/courier serviceability (note: takes a JSON body on a GET) |
| GET | `/api/v1/github/shiprocket/couriers` | Get recommended couriers (also takes a JSON body on GET) |
| POST | `/api/v1/github/shiprocket/awb` | Generate an AWB number |
| POST | `/api/v1/github/shiprocket/pickup` | Request a courier pickup |
| POST | `/api/v1/github/shiprocket/label` | Generate a shipping label |
| POST | `/api/v1/github/shiprocket/invoice` | Generate an invoice |
| POST | `/api/v1/github/shiprocket/manifest` | Generate a manifest |
| GET | `/api/v1/github/shiprocket/track/{awbCode}` | Track a shipment |
| POST | `/api/v1/github/shiprocket/cancel` | Cancel one or more orders |
| GET | `/api/v1/github/shiprocket/orders` | List Shiprocket orders |
| GET | `/api/v1/github/shiprocket/orders/{orderId}` | Get a Shiprocket order |
| PUT | `/api/v1/github/shiprocket/orders` | Update a Shiprocket order |
| GET | `/api/v1/github/shiprocket/pickup-locations` | List pickup locations |
| POST | `/api/v1/github/shiprocket/pickup-location` | Add a pickup location |
| GET | `/api/v1/github/shiprocket/channels` | List sales channels |
| GET | `/api/v1/github/shiprocket/courier-companies` | List courier companies |
| GET | `/api/v1/github/shiprocket/ndr` | List NDR (non-delivery) shipments |
| POST | `/api/v1/github/shiprocket/ndr` | Act on an NDR shipment (re-attempt/RTO) |

#### Bookings — `/bookings`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/bookings/` | Create a booking (worked example below) |
| GET | `/api/v1/github/bookings/` | List all |
| GET | `/api/v1/github/bookings/{bookingId}` | Get one |
| PUT | `/api/v1/github/bookings/{bookingId}` | Update (status, payment, amounts, approval) |
| DELETE | `/api/v1/github/bookings/{bookingId}` | Delete |

#### Booking Cancellations — `/booking-cancellations`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/booking-cancellations/` | Request cancellation |
| GET | `/api/v1/github/booking-cancellations/` | List all |
| GET | `/api/v1/github/booking-cancellations/{cancellationId}` | Get one |
| PUT | `/api/v1/github/booking-cancellations/{cancellationId}` | Update (approve/reject) |
| DELETE | `/api/v1/github/booking-cancellations/{cancellationId}` | Delete |

#### Booking Refunds — `/booking-refunds`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/booking-refunds/` | Create a refund record |
| GET | `/api/v1/github/booking-refunds/` | List all |
| GET | `/api/v1/github/booking-refunds/{refundId}` | Get one |
| PUT | `/api/v1/github/booking-refunds/{refundId}` | Update (status transitions) |
| DELETE | `/api/v1/github/booking-refunds/{refundId}` | Delete |

#### Booking Feedbacks — `/booking-feedbacks`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/booking-feedbacks/` | Submit feedback |
| GET | `/api/v1/github/booking-feedbacks/` | List all |
| GET | `/api/v1/github/booking-feedbacks/{feedbackId}` | Get one |
| PUT | `/api/v1/github/booking-feedbacks/{feedbackId}` | Update |
| DELETE | `/api/v1/github/booking-feedbacks/{feedbackId}` | Delete |

#### Appointments — `/appointments`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/appointments/` | Create an appointment |
| GET | `/api/v1/github/appointments/` | List all |
| GET | `/api/v1/github/appointments/{appointmentId}` | Get one |
| PUT | `/api/v1/github/appointments/{appointmentId}` | Update |
| DELETE | `/api/v1/github/appointments/{appointmentId}` | Delete |

#### Calendar — `/calendar`
Google Calendar-style OAuth stub.

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/github/calendar/` | Liveness check |
| GET | `/api/v1/github/calendar/login` | Get the OAuth consent URL |
| GET | `/api/v1/github/calendar/callback` | Exchange `code` for an access token — ⚠️ returns the raw token directly in the response body |

#### Offers — `/offers`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/offers/` | Create an offer (% or flat discount on product/service/category/store/coupon) |
| GET | `/api/v1/github/offers/` | List all |
| GET | `/api/v1/github/offers/{offerId}` | Get one |
| PUT | `/api/v1/github/offers/{offerId}` | Update |
| DELETE | `/api/v1/github/offers/{offerId}` | Delete |

#### Offer Targets — `/offer-targets`
Create/read/delete only.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/offer-targets/` | Attach a target to an offer |
| GET | `/api/v1/github/offer-targets/` | List all |
| GET | `/api/v1/github/offer-targets/{targetId}` | Get one |
| DELETE | `/api/v1/github/offer-targets/{targetId}` | Remove |

#### Offer Customer Segments — `/offer-customer-segments`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/offer-customer-segments/` | Restrict an offer to a customer group |
| GET | `/api/v1/github/offer-customer-segments/` | List all |
| GET | `/api/v1/github/offer-customer-segments/{segmentId}` | Get one |
| PUT | `/api/v1/github/offer-customer-segments/{segmentId}` | Update |
| DELETE | `/api/v1/github/offer-customer-segments/{segmentId}` | Delete |

#### Offer Exclusions — `/offer-exclusions`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/offer-exclusions/` | Create an exclusion rule |
| GET | `/api/v1/github/offer-exclusions/` | List all |
| GET | `/api/v1/github/offer-exclusions/{exclusionId}` | Get one |
| PUT | `/api/v1/github/offer-exclusions/{exclusionId}` | Update |
| DELETE | `/api/v1/github/offer-exclusions/{exclusionId}` | Delete |

#### Coupons — `/coupons`
Defines a coupon code tied to an offer. **Does not itself redeem/apply anything** — see Coupon Redemptions below for that.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/coupons/` | Create a coupon |
| GET | `/api/v1/github/coupons/` | List all |
| GET | `/api/v1/github/coupons/{couponId}` | Get one |
| PUT | `/api/v1/github/coupons/{couponId}` | Update |
| DELETE | `/api/v1/github/coupons/{couponId}` | Delete |

#### Coupon Redemptions — `/coupon-redemptions`
The route that actually applies a coupon (worked example below). ⚠️ Inserts directly with **no check that the coupon exists, no usage-limit enforcement, and no duplicate-redemption guard** — the `usage_limit`/`usage_limit_per_customer`/`first_time_customer_only` fields on `Coupon` are not enforced here.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/coupon-redemptions/` | Redeem a coupon against an order or booking |
| GET | `/api/v1/github/coupon-redemptions/` | List all |
| GET | `/api/v1/github/coupon-redemptions/{redemptionId}` | Get one |
| PUT | `/api/v1/github/coupon-redemptions/{redemptionId}` | Update |
| DELETE | `/api/v1/github/coupon-redemptions/{redemptionId}` | Delete |

#### Customers — `/customers`
This module's own storefront-customer record, separate from the platform `User` and from `customerEngine`. No get-by-id/update/delete route exists.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/customers/` | Create a customer |
| GET | `/api/v1/github/customers/store/{store_id}` | List customers for a store |

#### Authentication (secondary system) — `/auth`
⚠️ **Materially incomplete** — `POST /login` verifies the bcrypt password but **issues no token at all**; it cannot authenticate any subsequent request. `register` returns `400` (not `409`) on a duplicate email; `login` distinguishes 404 "user not found" from 401 "invalid password" (user-enumeration-friendly).

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/auth/register` | Register a user in this module's own `User` table |
| POST | `/api/v1/github/auth/login` | Log in — returns a success message + user fields, **no token** |

#### Notifications — `/notifications`
Persists notification *records* only — does not send anything itself.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/notifications/` | Queue a notification (EMAIL/SMS/WHATSAPP/IN_APP) |
| GET | `/api/v1/github/notifications/` | List all |
| GET | `/api/v1/github/notifications/{notificationId}` | Get one |
| PUT | `/api/v1/github/notifications/{notificationId}` | Update (mark sent/failed) |
| DELETE | `/api/v1/github/notifications/{notificationId}` | Delete |

#### OTP (secondary system) — `/otp`
A **second, independent OTP system** from the platform's main OTP flow — dev-grade: OTPs live in a plain in-process Python dict (`otp_store = {}`, no DB, no TTL, wiped on restart, not multi-worker safe). SMTP failures are silently swallowed — `send` always reports `{"success": true}` even if no email went out. `verify` returns `200 OK` with `{"success": false}` on a bad code rather than a 4xx.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/otp/send` | Generate and email a 6-digit code (worked example below) |
| POST | `/api/v1/github/otp/verify` | Verify a code for an email |

#### Wishlists — `/wishlists`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/wishlists/` | Create a wishlist |
| GET | `/api/v1/github/wishlists/` | List all |
| GET | `/api/v1/github/wishlists/{wishlistId}` | Get one |
| PUT | `/api/v1/github/wishlists/{wishlistId}` | Update |
| DELETE | `/api/v1/github/wishlists/{wishlistId}` | Delete |

#### Wishlist Items — `/wishlist-items`
Create/read/delete only.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/wishlist-items/` | Add a product to a wishlist |
| GET | `/api/v1/github/wishlist-items/` | List all |
| GET | `/api/v1/github/wishlist-items/{wishlistItemId}` | Get one |
| DELETE | `/api/v1/github/wishlist-items/{wishlistItemId}` | Remove |

#### Saved For Later — `/saved-for-later`
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/saved-for-later/` | Save a cart/product item |
| GET | `/api/v1/github/saved-for-later/` | List all |
| GET | `/api/v1/github/saved-for-later/{savedItemId}` | Get one |
| PUT | `/api/v1/github/saved-for-later/{savedItemId}` | Update |
| DELETE | `/api/v1/github/saved-for-later/{savedItemId}` | Delete |

#### Recently Viewed Products — `/recently-viewed-products`
Create/read/delete only.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/recently-viewed-products/` | Record a product view |
| GET | `/api/v1/github/recently-viewed-products/` | List all |
| GET | `/api/v1/github/recently-viewed-products/{recentlyViewedId}` | Get one |
| DELETE | `/api/v1/github/recently-viewed-products/{recentlyViewedId}` | Delete |

#### Product Compare Lists — `/product-compare-lists`
Create/read/delete only.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/product-compare-lists/` | Create a comparison list |
| GET | `/api/v1/github/product-compare-lists/` | List all |
| GET | `/api/v1/github/product-compare-lists/{compareListId}` | Get one |
| DELETE | `/api/v1/github/product-compare-lists/{compareListId}` | Delete |

#### Product Compare Items — `/product-compare-items`
Create/read/delete only.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/product-compare-items/` | Add a product to a compare list |
| GET | `/api/v1/github/product-compare-items/` | List all |
| GET | `/api/v1/github/product-compare-items/{compareItemId}` | Get one |
| DELETE | `/api/v1/github/product-compare-items/{compareItemId}` | Remove |

#### Products — `/products`
This module's own lightweight product record, used by wishlist/compare/recently-viewed.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/github/products/` | Create a product |
| GET | `/api/v1/github/products/` | List all |
| GET | `/api/v1/github/products/{productId}` | Get one |
| PUT | `/api/v1/github/products/{productId}` | Update |
| DELETE | `/api/v1/github/products/{productId}` | Delete |

#### Example — Create a Booking

```
POST /api/v1/github/bookings/
Content-Type: application/json

{
  "tenant_id": "11111111-1111-1111-1111-111111111111",
  "store_id": "22222222-2222-2222-2222-222222222222",
  "service_id": "33333333-3333-3333-3333-333333333333",
  "customer_id": "44444444-4444-4444-4444-444444444444",
  "booking_mode": "BOOK_AND_PAY",
  "booking_date": "2026-09-05",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "attendee_count": 2,
  "subtotal_amount": 1500.00,
  "discount_amount": 150.00,
  "tax_amount": 67.50,
  "currency_code": "INR"
}
```

```json
// 201 Created — booking_number is auto-generated, total_amount computed if omitted
{
  "id": "55555555-5555-5555-5555-555555555555",
  "booking_number": "BK-9F3A7C21",
  "booking_status": "PENDING",
  "payment_status": "PENDING",
  "booking_mode": "BOOK_AND_PAY",
  "booking_date": "2026-09-05",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "subtotal_amount": 1500.0,
  "discount_amount": 150.0,
  "tax_amount": 67.5,
  "total_amount": 1417.5,
  "currency_code": "INR",
  "booked_at": "2026-08-28T10:15:00Z"
}
```

```json
// 422 Unprocessable Entity — start_time >= end_time (model validator)
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [ { "type": "value_error", "loc": ["body"], "msg": "Value error, start_time must be before end_time" } ]
  }
}
```

#### Example — Redeem a Coupon

```
POST /api/v1/github/coupon-redemptions/
Content-Type: application/json

{
  "coupon_id": "66666666-6666-6666-6666-666666666666",
  "customer_id": "44444444-4444-4444-4444-444444444444",
  "booking_id": "55555555-5555-5555-5555-555555555555",
  "discount_amount": 150.00
}
```

```json
// 201 Created
{
  "id": "77777777-7777-7777-7777-777777777777",
  "coupon_id": "66666666-6666-6666-6666-666666666666",
  "customer_id": "44444444-4444-4444-4444-444444444444",
  "order_id": null,
  "booking_id": "55555555-5555-5555-5555-555555555555",
  "discount_amount": 150.0,
  "redeemed_at": "2026-08-28T10:16:00Z"
}
```

```json
// 422 — neither order_id nor booking_id supplied (model validator requires at least one)
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [ { "type": "value_error", "loc": ["body"], "msg": "Value error, Either order_id or booking_id must be provided" } ]
  }
}
```

#### Example — Send OTP

```
POST /api/v1/github/otp/send
Content-Type: application/json

{ "email": "priya.sharma@example.com" }
```
```json
// 200 OK — returned even if the underlying SMTP send silently failed
{ "success": true, "message": "OTP sent successfully" }
```

```
POST /api/v1/github/otp/verify
Content-Type: application/json

{ "email": "priya.sharma@example.com", "otp": "482913" }
```
```json
// 200 OK — a bad/expired code is NOT a 4xx here, just success:false
{ "success": false, "message": "Invalid OTP" }
```

### Service Engine (`/service-engine`)

A standalone module (`serviceEngine/`) for service-based businesses (salons, consultants, etc.) — service categories, services, booking rules, and weekly availability slots. Mounted directly in `app/api/router.py` (not under `/github`). Every route uses only `Depends(getDb)` — **all endpoints are Public (no auth)**. All not-found/conflict errors here use the plain `{"detail": "..."}` shape (manual `HTTPException`, not the platform's `NotFoundError`/`ConflictError`).

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/service-engine/categories` | Public | Create a service category; `400` on duplicate name/slug per tenant. |
| GET | `/api/v1/service-engine/categories` | Public | List active categories for a `tenantId` (required query param). |
| GET | `/api/v1/service-engine/categories/{categoryId}` | Public | Get a category. |
| PUT | `/api/v1/service-engine/categories/{categoryId}` | Public | Update; re-validates name/slug uniqueness. |
| DELETE | `/api/v1/service-engine/categories/{categoryId}` | Public | Soft-delete (`isActive=false`). |
| POST | `/api/v1/service-engine/services` | Public | Create a service; enforces the tenant's plan service-count limit (`PlanGuard.check_service_limit`), validates `serviceType` (`PHYSICAL`/`ONLINE`) and an active `categoryId`. |
| GET | `/api/v1/service-engine/services` | Public | List active services for a `tenantId` (required). |
| GET | `/api/v1/service-engine/services/{serviceId}` | Public | Get a service. |
| PUT | `/api/v1/service-engine/services/{serviceId}` | Public | Update service fields, re-validating type/category. |
| DELETE | `/api/v1/service-engine/services/{serviceId}` | Public | Soft-delete. |
| POST | `/api/v1/service-engine/services/{serviceId}/submit-approval` | Public | Set `approvalStatus="PENDING"`. |
| POST | `/api/v1/service-engine/booking-rules` | Public | Create or update (upsert) a service's booking mode (`BOOKING_ONLY`/`BOOKING_AND_PAYMENT`) and approval requirement. |
| GET | `/api/v1/service-engine/booking-rules/service/{serviceId}` | Public | Get the active booking rule for a service. |
| POST | `/api/v1/service-engine/booking-rules/validate-booking` | Public | Validate whether a booking can proceed: checks the tenant is active/not suspended, has an active plan mapping, the service is active, and (if `BOOKING_AND_PAYMENT`) that payment proof was supplied. |
| POST | `/api/v1/service-engine/availabilities` | Public | Create a weekly availability slot; validates `dayOfWeek` (0–6), `HH:MM` time format, `start < end`, and rejects overlapping slots for the same service+day. |
| GET | `/api/v1/service-engine/availabilities/service/{serviceId}` | Public | List active availability slots for a service. |
| PUT | `/api/v1/service-engine/availabilities/{availabilityId}` | Public | Update a slot; re-validates format/ordering/overlap. |
| DELETE | `/api/v1/service-engine/availabilities/{availabilityId}` | Public | Deactivate a slot. |

#### Example — Validate a Booking

```
POST /api/v1/service-engine/booking-rules/validate-booking
Content-Type: application/json

{
  "tenantId": "11111111-1111-1111-1111-111111111111",
  "serviceId": "22222222-2222-2222-2222-222222222222",
  "isPaid": true,
  "paymentReferenceId": "pay_9F3A7C21"
}
```

```json
// 200 OK
{ "status": "VALID", "requiresApproval": false }
```

```json
// 400 Bad Request — tenant has no active subscription plan
{ "detail": "Booking blocked: Service provider has no active plan" }
```

### Customer Engine (`/customer-engine`)

A standalone module (`customerEngine/`) for guest-checkout handling, customer-profile activation, and address management — with its own `bcrypt`-based password context (bypassing a `passlib`/`bcrypt` 4.x compatibility issue). Mounted directly in `app/api/router.py`. Every route uses only `Depends(getDb)` — **all endpoints are Public (no auth)**. Errors use the plain `{"detail": "..."}` shape.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/customer-engine/guest-checkout` | Public | Process a guest order: merges into an existing registered customer if email/mobile matches, reuses/updates an existing guest profile, or creates a new one — then stores the address and a `SUCCESS` order in one call. |
| POST | `/api/v1/customer-engine/customers/{customerId}/activate` | Public | Convert a guest profile into a full account by setting a password (`CUST-GUEST-...` code becomes `CUST-...`). |
| GET | `/api/v1/customer-engine/customers/{customerId}` | Public | Fetch a customer profile. |
| PUT | `/api/v1/customer-engine/customers/{customerId}` | Public | Update profile fields; validates duplicate email/mobile within the store. |
| POST | `/api/v1/customer-engine/customers/{customerId}/media` | Public | Upload a profile image (`multipart/form-data`) — note: this is a simulated/mocked path mapping, not real file storage. |
| POST | `/api/v1/customer-engine/customers/{customerId}/addresses` | Public | Add an address; clears other `isDefault` addresses of the same type if this one is default. |
| GET | `/api/v1/customer-engine/customers/{customerId}/addresses` | Public | List a customer's active addresses (default first, newest first). |
| PUT | `/api/v1/customer-engine/addresses/{addressId}` | Public | Update an address; re-applies the default-switching rule. |
| DELETE | `/api/v1/customer-engine/addresses/{addressId}` | Public | Hard-delete an address (no `isActive` column on this table). |

#### Example — Guest Checkout

```
POST /api/v1/customer-engine/guest-checkout
Content-Type: application/json

{
  "tenantId": "11111111-1111-1111-1111-111111111111",
  "storeId": "22222222-2222-2222-2222-222222222222",
  "firstName": "Kavya",
  "lastName": "Reddy",
  "email": "kavya.reddy@example.com",
  "mobile": "9988776655",
  "totalAmount": 2499.00,
  "address": {
    "addressType": "shipping",
    "fullName": "Kavya Reddy",
    "mobile": "9988776655",
    "addressLine1": "45 Jubilee Hills",
    "city": "Hyderabad",
    "state": "Telangana",
    "postalCode": "500033",
    "isDefault": true
  }
}
```

```json
// 201 Created
{
  "message": "Guest checkout successful",
  "customer": {
    "id": "33333333-3333-3333-3333-333333333333",
    "customerCode": "CUST-GUEST-7A1B2C",
    "firstName": "Kavya",
    "lastName": "Reddy",
    "email": "kavya.reddy@example.com",
    "mobile": "9988776655",
    "isGuestCustomer": true,
    "status": "ACTIVE"
  },
  "order": {
    "id": "44444444-4444-4444-4444-444444444444",
    "orderNumber": "ORD-9F3A7C21",
    "totalAmount": 2499.00,
    "status": "SUCCESS"
  }
}
```

---

## Known Issues & Caveats

This section was compiled while writing the API reference above, by reading every router in the codebase. It's here so integrators know what to double-check rather than discovering it in production.

### Security

- **Hardcoded credentials in source (critical):** `app/productsPorted/core/config.py` ships a live-looking Dropbox access token and a Neon PostgreSQL connection string (with embedded password) as literal default values, not just as example placeholders. Treat both as compromised — rotate the Dropbox token and the database password, and set real values only via `.env`/deployment secrets, never in the file itself. Do this before doing anything else with this repo.
- **Two large modules are entirely unauthenticated.** The whole `/api/v1/github/*` ported commerce suite (carts, orders, payments, shipping, bookings, offers, coupons, wishlist — over 300 routes) and the whole Ported Product Catalog (`/api/v1/catalog/*`) have **zero** routes protected by `getCurrentUserId`/`getCurrentUserWithRole`/`require_role`/`require_permission`. The same is true for most of Customers, most of the Website Builder (including bank-account CRUD), most of Approvals/Auditing, and several Tenant/Plan/Billing endpoints (see the per-section auth notes above for exactly which ones). If any of this is meant to be tenant-, store-, or ownership-scoped, that enforcement does not currently exist at the API layer.
- **`POST /api/v1/auth/token` mints access+refresh tokens for any `userId` string with no credential check at all.** It predates the OTP-based login flow and looks like a leftover dev/testing stub — don't expose it publicly.
- **`POST /api/v1/github/auth/login` never issues a token.** It only verifies the bcrypt password and echoes back user fields — there is nothing a client could use as a bearer credential from this endpoint, so nothing downstream in that module can actually be gated by it even if someone tried.
- **Two dev-grade, in-memory OTP stores exist besides the main one:** `app/services/github/otpService.py` (`/api/v1/github/otp/*`) keeps OTPs in a plain Python dict with no TTL, no persistence across restarts, and swallows SMTP errors while still reporting success. Don't rely on either of the `github` OTP/auth systems for anything security-sensitive.
- **The JWT revocation list is in-memory and single-process** (`app/core/tokenBlacklist.py`) — logout-based revocation does not survive a restart and does not work across multiple server replicas/workers.
- **CORS is wide open** (`allow_origins=["*"]` with `allow_credentials=True` in `app/main.py`) — flagged in the source itself as a `TODO`. Restrict this before production.

### Correctness bugs

- **`features.py` and `billingRules.py` double the API prefix.** Both files declare `APIRouter(tags=[...])` with no prefix but hardcode absolute paths starting with `/api/v1/...` in their route decorators. Since the whole `apiRouter` is itself mounted at `/api/v1`, the paths these routers actually serve are `/api/v1/api/v1/...` (documented as such above, under [Tenants & Subscriptions](#tenants--subscriptions)).
- **`POST /api/v1/stores/{storeId}/submit` always 500s.** `StoreService.submitForApproval` is accidentally defined as a nested function inside `deleteStore()` in `app/services/storeService.py` (an indentation bug), so it isn't a real method on the class — every call raises `AttributeError`.
- **`POST /api/v1/stores/{storeId}/generate-ai` always 500s.** `StoreService` has no `generateAI` method anywhere.
- **`stores.py` has a dead duplicate route.** `PATCH /{storeId}/theme` is registered twice as two separate functions named `changeTheme`; only the first (with a `response_model`) ever serves traffic.
- **`app/productsPorted/routers/products.py` and several other routers manually catch `SQLAlchemy IntegrityError`** and re-raise generic messages, while the `/github` order/payment routers rely entirely on the *global* `IntegrityError` handler — meaning a duplicate `order_number` and a bad foreign key both collapse into the same generic `"Database constraint violation..."` message with no indication of which field was the problem.
- **`POST /api/v1/github/checkout` does not create an order**, despite the name — it only computes and returns totals from the already-stored cart. The real order-creation call is `POST /api/v1/github/orders/`.
- **`POST /api/v1/github/coupon-redemptions/` enforces none of the coupon's own business rules** (`usage_limit`, `usage_limit_per_customer`, `first_time_customer_only`) and doesn't verify the referenced `coupon_id` exists before inserting.
- **`review-queue/bulk-action` never surfaces an HTTP error**, even for real per-item failures — every failure mode is folded into a `200 OK` response with a `"FAILED"` status string per item, so naive callers that only check the HTTP status code will treat partial/total failures as success.

### API consistency

- **Three different error-body shapes coexist**, and which one you get depends on the specific endpoint, not just the failure type:
  1. `{"error": {"code": "...", "message": "..."}}` — auto-generated for `AppException` subclasses that reach the global handler unmodified.
  2. `{"detail": "..."}` — FastAPI's default, produced whenever a router manually raises `HTTPException` (the majority of routers in this codebase do this, even ones importing `NotFoundError`/`ConflictError` — several routers catch those and re-wrap them as `HTTPException`, discarding the structured shape).
  3. `{"detail": {...structured object...}}` — used uniquely by `PlanLimitExceeded` (`app/core/planGuard.py`), where `detail` is a dict, not a string.
  Always branch on response body content, not on an assumed shape.
- **Two independent "auth" systems beyond the main platform JWT**: the Live Chat `ChatUser`/Chat-JWT system (`app/core/securityChat.py`), and the `/api/v1/github/auth` system (which, per above, issues no token at all). None of the three are interchangeable.
- **REST shape inconsistencies**: several endpoints accept what would normally be a path parameter as a query parameter instead (`PATCH /stores/{storeId}/theme?themeId=`, `PUT /websites/update?websiteId=`, `POST /website-deployments/{id}/success?deploymentUrl=`, two Shiprocket `GET` routes that require a JSON body). `publicWebsite.py` mounts a route at the bare API root (`GET /api/v1/`) since it declares no router prefix.

### Fixed while writing this README

- `Procfile` referenced a stale `src.main:app` module path (predating a rename to `app/`) and had a stray leftover `cat requirements.txt` appended to the line — corrected to `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`, matching the `Dockerfile`'s entry point.
- `.env.example` was missing entries for roughly a dozen environment variables the code actually reads (Razorpay, Google Calendar OAuth, Shiprocket, Cerebras/Tavily for the blog agent, the legacy `EMAIL_ADDRESS`/`EMAIL_PASSWORD` pair, and the entire separate `productsPorted` settings class) — all added with placeholder values.

## Module Ownership

File headers across the codebase carry `# Owner: <email>` (or a name) comments indicating who authored/maintains that module. For context when navigating the code:

| Owner | Scope |
|---|---|
| mousamdas156@gmail.com | Core application foundation — `app/main.py`, `app/core/*`, `app/db/*`, most of `app/api/v1/endpoints/*`, `app/schemas/*` (auth, users, tenants, catalog, media, approvals, chat, invoicing, blog agent) |
| Shlok Pallav (shlokpallav@gmail.com) | The entire ported e-commerce suite under `app/api/v1/endpoints/github/`, `app/controllers/github/`, `app/repositories/github/`, `app/schemas/github/`, `app/services/github/` (carts, orders, payments, shipping, bookings, offers, wishlist, and the secondary auth/OTP systems) |
| pradhansaikat123@gmail.com | `app/productsPorted/*` (ported product catalog module), `serviceEngine/`, `customerEngine/`, plus contributions across `app/api/`, `app/db/models/`, `app/schemas/` |

This is informational only — it reflects file-header comments as of this README's generation, not a live org chart.


# API Router Mapping — ACTIVE / DEPRECATED / INTERNAL

Ground truth for which router owns which URL prefix when more than one
module claims the same domain. Backend is FastAPI; every router listed here
is mounted simultaneously in `app/api/router.py` — nothing is conditionally
excluded at runtime, so "duplicate" means *literally two live endpoints*,
not two code paths where only one is wired up.

Legend:
- **ACTIVE** — the router the frontend should call. New integration work goes here.
- **DEPRECATED** — still mounted and working (for backward compatibility with
  whatever already calls it) but flagged `deprecated=True` in the OpenAPI
  schema (renders struck-through in Swagger/ReDoc) and must not be used for
  new integration.
- **INTERNAL** — not a competitor to the ACTIVE router; a different concern
  that happens to share a URL segment name.

Detail docs: [`customers.md`](./customers.md) · [`auth.md`](./auth.md) · [`catalog.md`](./catalog.md)

## Quick reference

| Domain | ACTIVE | DEPRECATED | INTERNAL |
|---|---|---|---|
| Auth | `POST /api/v1/auth/register`, `/auth/login` (+ OTP verify) | `POST /api/v1/github/auth/register`, `/github/auth/login` | `POST /api/v1/chat-auth/*` (live-chat widget only) |
| Customers | `/api/v1/customers/*` | `/api/v1/customer-engine/customers/{id}` (GET/PUT), `/customer-engine/addresses/*`, `/customer-engine/customers/{id}/addresses` | `/api/v1/customer-engine/guest-checkout`, `/activate`, `/media` (no ACTIVE equivalent) |
| Customer addresses | `/api/v1/addresses/*` | (see customer-engine address routes above) | — |
| Brands / Categories | `/api/v1/brands`, `/api/v1/categories` | none removed | `/api/v1/catalog/brands`, `/api/v1/catalog/categories` — different DB engine, see catalog.md |

## Enforcement mechanism used

FastAPI's own `deprecated=True` flag (per-route or on `include_router(...,
deprecated=True)`) rather than a hand-rolled route-guard middleware. Reasons:

1. It's inspected by FastAPI itself and shows up correctly in the generated
   `openapi.json` (`"deprecated": true` per operation) — any OpenAPI-aware
   frontend codegen (orval, openapi-typescript, swagger-codegen) picks it up
   automatically and marks the generated client method deprecated, which is
   the actual goal ("frontend calls never hit dead endpoints" — the frontend
   tooling warns at generation time instead of at request time).
2. A route-guard middleware that 404s deprecated paths would break whatever
   currently depends on them with no migration window — a harder break than
   the ask requires. `deprecated=True` keeps them working while making them
   visibly wrong to reach for.
3. If/when you're ready for a hard cutover, flip specific routes from
   `deprecated=True` to actually removed — that's a one-line diff per route
   once traffic to them is confirmed at zero (check access logs / APM by
   path, not just by "the flag is set").

See `app/schemas/common.py` (`APIResponse[T]`) and `app/core/exceptions.py`
for the standardized envelope — `{success, data, message}` on success,
`{success: false, error: {code, message, details?}}` on failure (extends the
existing error contract with `success` rather than replacing `error.code` /
`error.message`, which other code may already depend on).

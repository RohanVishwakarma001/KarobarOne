# Catalog: Brands & Categories — router mapping

| Router | Prefix | DB engine/session | Model base | Status |
|---|---|---|---|---|
| `app/api/v1/endpoints/brands.py`, `categories.py` | `/api/v1/brands`, `/api/v1/categories` | `app.db.session.getDb` — main app engine (`app.core.config.settings.databaseUrl`) | `app.db.base.Base` | **ACTIVE** |
| `app/productsPorted/routers/brands.py`, `categories.py` (+ products/variants/attributes/images/shipping) | `/api/v1/catalog/brands`, `/api/v1/catalog/categories`, ... | `app.productsPorted.core.database.get_db` — a **second, independently-created** `create_async_engine` | `app.productsPorted.core.database.Base` (separate `DeclarativeBase`) | **INTERNAL — see below, do not treat as interchangeable** |

## This is not a routing duplicate, it's a second database connection

`app/productsPorted/core/database.py` builds its own engine from
`app.productsPorted.core.config.Settings`, a **separate** Pydantic settings
class from `app.core.config.Settings` (the one every other router uses).
Both read `DATABASE_URL` from the environment via `validation_alias`, so *if
that env var is set*, both engines point at the same Postgres instance and
the two `brands` table definitions (`app/db/models/brands.py` vs
`app/productsPorted/models/models.py`, both `__tablename__ = "brands"`) are
two independent ORM mappings of the same physical table — the same failure
mode documented for `github.customer` in `customers.md`.

**Until this pass**, `app/productsPorted/core/config.py` had a hardcoded
production Neon Postgres connection string (with a real password) and a
real Dropbox access token as the *default value* of `databaseUrl` /
`dropboxAccessToken` — meaning any environment that didn't set
`DATABASE_URL` (e.g. a developer's laptop with a bare `.env` that only
configures the main app) would have silently connected `/api/v1/catalog/*`
straight to the production database while everything else on that machine
ran against local SQLite. That default has been removed in this pass
(`databaseUrl`, `secretKey`, and `dropboxAccessToken` are now required, no
fallback — the app fails fast at startup instead of silently reaching a
prod database from a dev box). **The exposed credentials were committed to
git and must be rotated** (new Neon password, new Dropbox token) —
removing the hardcoded default does not undo the exposure in git history.

## Recommendation (not yet done — needs a decision)

Given brands/categories/products/variants/attributes/images/shipping are all
namespaced under `/catalog` and appear to be the actively-developed product
catalog (it's the only one of the two with variants/attributes/images —
`app/db/models/brands.py`'s sibling `categories.py` has no product/variant
system at all), the standalone `/api/v1/brands` + `/api/v1/categories`
routers look like the earlier, narrower implementation that `/catalog/*`
was meant to supersede. Confirm which one the frontend/store-admin currently
writes to in production before marking either `deprecated=True` — unlike
`customers.py` and the github routers, these two are NOT proven to share a
table via the same engine in every environment, so flipping the flag on the
wrong one risks masking real, separately-stored data rather than just
duplicate routes.

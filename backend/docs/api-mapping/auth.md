# Auth — router mapping

| Router | Prefix | Session type | User table | Token issuer | Status |
|---|---|---|---|---|---|
| `app/api/v1/endpoints/auth.py` | `/api/v1/auth` | async | `app.db.models.user` (platform staff/store users) | `app.core.security.createAccessToken/createRefreshToken` | **ACTIVE** |
| `app/api/v1/endpoints/github/authRouter.py` | `/api/v1/github/auth` | **sync** (`Session`, `getSyncDb`) | `app.services.github.authService` → its own `users` table | separate, inside `authService` | **DEPRECATED** |
| `app/api/v1/endpoints/chatAuth.py` | `/api/v1/chat-auth` | async | `app.db.models.chatUser.ChatUser` | `app.services.authService.AuthService` | **INTERNAL** |

## Which one is the real session/JWT flow

`/api/v1/auth` is it. Every staff/admin-facing router in this codebase
(`users`, `roles`, `permissions`, `stores`, and now the customer admin
endpoints in `customers.py`) authenticates via `Depends(getCurrentUserId)` /
`Depends(getCurrentUserWithRole)` in `app/core/dependencies.py`, which calls
`app.core.security.decodeToken` — the same module `auth.py`'s
`login`/`register` flow issues tokens from. It's also the only one of the
three that's OTP-gated end to end (register → email OTP → verify → login →
email OTP → verify → tokens), matching the module docstring.

`/api/v1/github/auth` is not a variant of the same flow — it's a
**synchronous** SQLAlchemy path (`Session`, not `AsyncSession`; see
`getSyncDb` vs `getDb`) issuing tokens for a completely separate `users`
table via `app/services/github/authService.py`. A token minted there is not
decodable by `getCurrentUserId`/`decodeToken` unless the two token schemes
happen to agree by coincidence — treat it as a different identity system
that happens to share the path segment `/auth`. Deprecated in this pass (see
`app/api/v1/endpoints/github/__init__.py`) rather than removed, since other
`/github/*` routers may reference `customer_id`/`user_id` UUIDs that
originated from it — same reasoning as `customers.md`.

`/api/v1/chat-auth` is not a competitor at all: it authenticates the
**live-chat widget**, backed by `ChatUser`, mounted separately at
`/chat-ui` (`app/main.py`, `StaticFiles`). It was never meant to issue the
platform's session tokens, so there's nothing to deprecate — just don't
confuse "Chat Authentication" in the tag list for a third general-purpose
login endpoint.

## What changed in this pass

Only the routing/deprecation flag in `github/__init__.py` — see
`customers.md` for the mechanism (`deprecated=True` at
`include_router(authRouter, deprecated=True)`, pulled out of the bulk mount
loop). No schema or dependency changes were made to `auth.py` itself; it
already matches the pattern (`APIResponse`, `getCurrentUserId`,
`app.core.exceptions`) applied to `customers.py` in this pass — see
`app/core/dependencies.py` and `app/core/security.py` if you want to extend
the envelope there too.

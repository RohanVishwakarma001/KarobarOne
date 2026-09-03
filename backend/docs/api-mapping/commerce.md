# Cart, Orders & Payments — router mapping

## The two implementations

| Concern | ACTIVE | DEPRECATED |
|---|---|---|
| Cart | `/api/v1/cart/*` (`app/api/v1/endpoints/cart.py`) | `/api/v1/github/cart/*`, `cart-items/*`, `cart-coupons/*`, `abandoned-carts/*`, `checkout/*` |
| Orders | `/api/v1/orders/*` (`app/api/v1/endpoints/orders.py`) | `/api/v1/github/orders/*`, `order-items/*`, `order-status/*`, `order-cancellations/*` |
| Payments | `/api/v1/payments/razorpay/*` (`app/api/v1/endpoints/payments.py`) | `/api/v1/github/payments/*`, `payment-methods/*`, `payment-refunds/*` |

**Both read and write the same physical tables** (`carts`, `cart_items`, `orders`, `order_items`, `payments`, ...) — the ACTIVE routers reuse the existing `app/db/models/github/*` models via the main app's async session rather than introducing a second set of tables. This was a deliberate choice: the alternative (new tables) would have recreated the exact customers/brands-style data-fork this repo already has too much of — see `customers.md` and `catalog.md`.

What actually changed is the router layer:

| | DEPRECATED (github) | ACTIVE |
|---|---|---|
| Session type | sync (`getSyncDb`) | async (`getDb`) |
| Auth on cart/checkout | none | none (unavoidable — no customer JWT exists anywhere, see `auth.md`; tenant scoping instead comes from required `tenantId`/`storeId` params, validated against every row touched) |
| Auth on order status / refunds | none | staff bearer + tenant header (`getCurrentUserId` + `getTenantIdAsUUID`, same pattern as `customers.py`) |
| `GET /cart` | returns every cart, every tenant, no filter | scoped to `tenantId` + `storeId` + `customerId`/`sessionId` |
| Order status transitions | freeform string write | validated state machine (below), rejected with 400 otherwise |
| Razorpay order creation | `services/github/razorpayService.py`: on any error or missing credentials, silently fabricates a plausible-looking `order_mock_*` response | `services/razorpayClient.py`: raises `PaymentGatewayNotConfigured` (500) or `PaymentGatewayError` (502) — never fakes success |
| Razorpay signature verification | returns `True` unconditionally when credentials aren't configured | raises `PaymentGatewayNotConfigured` when unconfigured; otherwise a real `hmac.compare_digest` check, always |
| Razorpay webhook receiver | doesn't exist | `POST /payments/razorpay/webhook` — HMAC-verified against `X-Razorpay-Signature`, idempotent via `GatewayWebhookEvent.event_id`'s UNIQUE constraint |
| Idempotency | none | create-order reuses an existing `PENDING` `Payment` row for the same order instead of minting a second Razorpay order; verify short-circuits if already `SUCCESS`; webhook duplicates hit the unique-constraint path above |

With `razorpayKeyId`/`razorpayKeySecret`/`razorpayWebhookSecret` unset (as they are in this environment's `.env`), the ACTIVE payments router now fails closed on every gateway call instead of the old fail-open behavior — verified live: `POST /payments/razorpay/create-order` returns `500 PAYMENT_GATEWAY_NOT_CONFIGURED`, not a fabricated order.

## Order status state machine

This module implements the exact 6-state flow requested — not the more granular set `services/github/orderStatusService.py` already validates (`PACKED`, `OUT_FOR_DELIVERY`, etc.). Both are legitimate state machines for different granularity; this one is deliberately the simpler public contract:

```
PENDING → PAID → PROCESSING → SHIPPED → DELIVERED
   ↓         ↓         ↓
CANCELLED CANCELLED CANCELLED
```

Every transition is recorded to `app.db.models.approvals.StatusHistory` (`entityType="ORDER"`) — this is what backs the frontend's order-tracking timeline widget (`GET /orders/{id}/history`, no auth required, guest-trackable by order id).

## Two bugs found and fixed along the way (not new to this pass)

- `AuditLog.__tablename__` was `"audit_logs"`; the real table is `"auditLogs"`. Every `AuditLog()` insert anywhere in the app — not just here — has always raised `UndefinedTableError`. Fixed at the model level (`app/db/models/approvals.py`), which also fixes the try/except-guarded audit logging in `productsPorted/routers/products.py` from an earlier pass — those were working around the symptom, this fixes the cause.
- `StatusHistory.__tablename__` had the identical bug (`"status_history"` vs real `"statusHistory"`) — fixed the same way. Without this fix, the order-tracking timeline this module depends on would have silently never persisted anything.
- A subtler one, specific to this pass: building a Pydantic response from an ORM object *after* a second, best-effort `db.commit()` (the audit-log helper) intermittently raised `MissingGreenlet` — `expire_on_commit`'s default expires every attribute on commit, and a plain `db.get()` afterward doesn't reliably force the async-aware refresh needed before Pydantic's synchronous `getattr()` touches it. Fixed via `populate_existing=True` on the relevant `db.get()` calls plus eager `Model.model_validate()` before any later nested commit — see the comments on `orders.py::_loadOrderWithItems` and the two `refundPayment`/`verifyRazorpayPayment` call sites for the specifics.

## Not done in this pass

- `orderReturnRouter`, `paymentAuditLogRouter`, `subscriptionPaymentRouter`, and the gateway settlement/reconciliation routers have no ACTIVE equivalent and remain mounted normally (not deprecated).
- Coupon/offer *management* (creating offers and coupons) still goes through the github `couponRouter`/`offerRouter` — the ACTIVE `cart.py` only *consumes* coupons, it doesn't manage them.
- Cart items and orders reference `productId`/`productVariantId` as bare UUIDs with no FK to any specific catalog — same situation as before this pass (see `catalog.md`). `addCartItem` requires the caller to pass `unitPrice` explicitly rather than trusting a client-supplied price for the *stored* total (the router always recomputes line/cart totals server-side from stored data), but there's no live price lookup against `productsPorted` yet to validate that price against a real listing.

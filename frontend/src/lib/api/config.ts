const rawBaseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/** Base URL for the ported commerce suite (`/api/v1/github/*`) — unauthenticated per backend README. */
export const GITHUB_API_BASE_URL = `${rawBaseUrl.replace(/\/$/, "")}/api/v1/github`;

export const TENANT_ID = process.env.NEXT_PUBLIC_TENANT_ID ?? "";
export const STORE_ID = process.env.NEXT_PUBLIC_STORE_ID ?? "";

/** Public Razorpay key for Checkout.js (never the key secret — that stays server-side). */
export const RAZORPAY_KEY_ID = process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID ?? "";

/**
 * cart/order/payment/notification creation all require tenant_id + store_id.
 * There is no session that carries these (the module has no auth), so they come
 * from build-time config. Throws early with a clear message instead of letting
 * the backend reject with an opaque 422.
 */
export function assertStoreConfig(): void {
  if (!TENANT_ID || !STORE_ID) {
    throw new Error(
      "NEXT_PUBLIC_TENANT_ID / NEXT_PUBLIC_STORE_ID are not set. Copy .env.example to .env.local and fill in real values for the store this storefront serves."
    );
  }
}

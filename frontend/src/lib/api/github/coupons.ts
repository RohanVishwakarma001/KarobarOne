import { apiGet, apiPost, apiPut, apiDelete } from "../client";

export interface Coupon {
  id: string;
  offer_id: string;
  coupon_code: string;
  usage_limit?: number | null;
  usage_limit_per_customer?: number | null;
  first_time_customer_only: boolean;
  created_at: string;
  updated_at: string;
}

export interface CouponRedemption {
  id: string;
  coupon_id: string;
  customer_id: string;
  order_id?: string | null;
  booking_id?: string | null;
  discount_amount: number;
  redeemed_at: string;
}

/** Does not itself redeem/apply anything — see redeemCoupon() for that. */
export const createCoupon = (input: {
  offer_id: string;
  coupon_code: string;
  usage_limit?: number;
  usage_limit_per_customer?: number;
  first_time_customer_only?: boolean;
}) => apiPost<Coupon>("/coupons/", { first_time_customer_only: false, ...input });
// No code-lookup filter server-side — list all and match coupon_code client-side.
export const listCoupons = () => apiGet<Coupon[]>("/coupons/");
export const getCoupon = (couponId: string) => apiGet<Coupon>(`/coupons/${couponId}`);
export const updateCoupon = (
  couponId: string,
  data: Partial<Pick<Coupon, "offer_id" | "coupon_code" | "usage_limit" | "usage_limit_per_customer" | "first_time_customer_only">>
) => apiPut<Coupon>(`/coupons/${couponId}`, data);
export const deleteCoupon = (couponId: string) => apiDelete<void>(`/coupons/${couponId}`);

/**
 * The route that actually applies a coupon. ⚠️ Inserts directly with no check
 * that the coupon exists, no usage-limit enforcement, and no duplicate guard —
 * usage_limit / usage_limit_per_customer / first_time_customer_only on Coupon
 * are NOT enforced server-side (per backend README known-issues). The frontend
 * must check those rules itself before calling this.
 */
export const redeemCoupon = (input: { coupon_id: string; customer_id: string; order_id?: string; booking_id?: string; discount_amount: number }) =>
  apiPost<CouponRedemption>("/coupon-redemptions/", input);
export const listCouponRedemptions = () => apiGet<CouponRedemption[]>("/coupon-redemptions/");
export const getCouponRedemption = (redemptionId: string) => apiGet<CouponRedemption>(`/coupon-redemptions/${redemptionId}`);
export const updateCouponRedemption = (redemptionId: string, data: Partial<Pick<CouponRedemption, "order_id" | "booking_id" | "discount_amount">>) =>
  apiPut<CouponRedemption>(`/coupon-redemptions/${redemptionId}`, data);
export const deleteCouponRedemption = (redemptionId: string) => apiDelete<void>(`/coupon-redemptions/${redemptionId}`);

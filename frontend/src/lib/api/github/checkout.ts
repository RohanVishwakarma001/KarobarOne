import { apiPost } from "../client";

export interface CheckoutSummary {
  cart_id: string;
  total_items: number;
  subtotal: number;
  discount: number;
  shipping: number;
  tax: number;
  grand_total: number;
  currency: string;
}

/** Totals preview only — does NOT create an order. See orders.ts createOrder for that. */
export const previewCheckout = (input: { customer_id: string; shipping_address_id?: string; coupon_code?: string }) =>
  apiPost<CheckoutSummary>("/checkout", input);

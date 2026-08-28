import { apiGet, apiPost, apiPut, apiDelete } from "../client";
import { TENANT_ID, STORE_ID, assertStoreConfig } from "../config";

export interface Cart {
  id: string;
  tenant_id: string;
  store_id: string;
  customer_id?: string | null;
  session_id?: string | null;
  cart_status: string;
  subtotal_amount: number;
  discount_amount: number;
  tax_amount: number;
  shipping_amount: number;
  total_amount: number;
  currency_code: string;
  expires_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CartItem {
  id: string;
  cart_id: string;
  product_id: string;
  product_variant_id?: string | null;
  quantity: number;
  unit_price: number;
  discount_amount: number;
  tax_amount: number;
  line_total: number;
  added_at: string;
  updated_at: string;
}

export interface CartCoupon {
  id: string;
  cart_id: string;
  coupon_id: string;
  discount_amount: number;
  applied_at: string;
}

// No GET /cart?customer_id= filter exists server-side — callers must cache the
// created cartId (see useCart) rather than re-querying by customer.
export function createCart(customerId?: string) {
  assertStoreConfig();
  return apiPost<Cart>("/cart/", {
    tenant_id: TENANT_ID,
    store_id: STORE_ID,
    customer_id: customerId,
    cart_status: "ACTIVE",
  });
}

export const listCarts = () => apiGet<Cart[]>("/cart/");
export const getCart = (cartId: string) => apiGet<Cart>(`/cart/${cartId}`);
export const updateCart = (
  cartId: string,
  data: Partial<Pick<Cart, "cart_status" | "subtotal_amount" | "discount_amount" | "tax_amount" | "shipping_amount" | "total_amount" | "expires_at">>
) => apiPut<Cart>(`/cart/${cartId}`, data);
export const deleteCart = (cartId: string) => apiDelete<void>(`/cart/${cartId}`);

export interface AddCartItemInput {
  cart_id: string;
  product_id: string;
  product_variant_id?: string;
  quantity?: number;
  unit_price: number;
  discount_amount?: number;
  tax_amount?: number;
}
export const addCartItem = (input: AddCartItemInput) =>
  apiPost<CartItem>("/cart-items/", { quantity: 1, discount_amount: 0, tax_amount: 0, ...input });
export const listCartItems = (cartId: string) => apiGet<CartItem[]>(`/cart-items/by-cart/${cartId}`);
export const updateCartItem = (cartItemId: string, data: Partial<Pick<CartItem, "quantity" | "discount_amount" | "tax_amount">>) =>
  apiPut<CartItem>(`/cart-items/${cartItemId}`, data);
export const removeCartItem = (cartItemId: string) => apiDelete<void>(`/cart-items/${cartItemId}`);

export const listCartCoupons = () => apiGet<CartCoupon[]>("/cart-coupons/");
export const applyCartCoupon = (input: { cart_id: string; coupon_id: string; discount_amount: number }) =>
  apiPost<CartCoupon>("/cart-coupons/", input);
export const removeCartCoupon = (cartCouponId: string) => apiDelete<void>(`/cart-coupons/${cartCouponId}`);

// ---------------------------------------------------------------------------
// Abandoned Carts — recovery-campaign tracking, not customer-facing.
// ---------------------------------------------------------------------------

export type RecoveryStatus = "PENDING" | "RECOVERED" | "EXPIRED";
export interface AbandonedCart {
  id: string;
  cart_id: string;
  customer_id?: string | null;
  recovery_status?: RecoveryStatus | null;
  reminder_sent_count?: number | null;
  last_reminder_sent_at?: string | null;
  recovered_at?: string | null;
  created_at?: string | null;
}
export const recordAbandonedCart = (input: { cart_id: string; customer_id?: string; recovery_status?: RecoveryStatus }) =>
  apiPost<AbandonedCart>("/abandoned-carts/", { recovery_status: "PENDING", ...input });
export const listAbandonedCarts = () => apiGet<AbandonedCart[]>("/abandoned-carts/");
export const getAbandonedCart = (abandonedCartId: string) => apiGet<AbandonedCart>(`/abandoned-carts/${abandonedCartId}`);
export const updateAbandonedCart = (abandonedCartId: string, data: { recovery_status?: RecoveryStatus; recovered_at?: string }) =>
  apiPut<AbandonedCart>(`/abandoned-carts/${abandonedCartId}`, data);
export const deleteAbandonedCart = (abandonedCartId: string) => apiDelete<void>(`/abandoned-carts/${abandonedCartId}`);

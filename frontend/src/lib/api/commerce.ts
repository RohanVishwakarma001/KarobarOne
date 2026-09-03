import { apiDelete, apiGet, apiPatch, apiPost } from "./api-client";

// ============================================================================
// Types — mirror app/schemas/commerce.py exactly (the ACTIVE backend module;
// see docs/api-mapping/commerce.md — NOT lib/api/github/{cart,orders,payments}.ts,
// which point at the deprecated github-ported routers)
// ============================================================================

export type CartStatus = "ACTIVE" | "CONVERTED" | "ABANDONED" | "EXPIRED";

export type CartItem = {
  id: string;
  productId: string;
  productVariantId: string | null;
  quantity: number;
  unitPrice: string;
  discountAmount: string;
  taxAmount: string;
  lineTotal: string;
};

export type Cart = {
  id: string;
  tenantId: string;
  storeId: string;
  customerId: string | null;
  sessionId: string | null;
  status: CartStatus;
  subtotalAmount: string;
  discountAmount: string;
  taxAmount: string;
  shippingAmount: string;
  totalAmount: string;
  currencyCode: string;
  items: CartItem[];
};

export type OrderStatus = "PENDING" | "PAID" | "PROCESSING" | "SHIPPED" | "DELIVERED" | "CANCELLED";

export const ORDER_STATUS_SEQUENCE = ["PENDING", "PAID", "PROCESSING", "SHIPPED", "DELIVERED"] as const;

export type OrderItemInput = {
  productId: string;
  productVariantId?: string;
  sku: string;
  productName: string;
  variantName?: string;
  quantity: number;
  unitPrice: number;
  taxAmount?: number;
  discountAmount?: number;
};

export type OrderItem = {
  id: string;
  productId: string;
  productVariantId: string | null;
  sku: string;
  productName: string;
  variantName: string | null;
  quantity: number;
  unitPrice: string;
  discountAmount: string;
  taxAmount: string;
  lineTotal: string;
};

export type Order = {
  id: string;
  tenantId: string;
  storeId: string;
  customerId: string;
  orderNumber: string;
  billingAddressId: string;
  shippingAddressId: string;
  orderStatus: OrderStatus;
  paymentStatus: string;
  fulfillmentStatus: string;
  subtotalAmount: string;
  discountAmount: string;
  taxAmount: string;
  shippingAmount: string;
  totalAmount: string;
  currencyCode: string;
  customerNote: string | null;
  placedAt: string | null;
  createdAt: string | null;
  updatedAt: string | null;
  items: OrderItem[];
};

export type OrderStatusEvent = {
  oldStatus: string | null;
  newStatus: string;
  changeReason: string | null;
  changedAt: string | null;
};

export type CreateRazorpayOrderResult = {
  razorpayOrderId: string;
  razorpayKeyId: string;
  amount: number;
  currency: string;
  paymentId: string;
};

// ============================================================================
// Cart
// ============================================================================

export function getCart(params: { tenantId: string; storeId: string; customerId?: string; sessionId?: string }): Promise<Cart> {
  const qs = new URLSearchParams({ tenantId: params.tenantId, storeId: params.storeId });
  if (params.customerId) qs.set("customerId", params.customerId);
  if (params.sessionId) qs.set("sessionId", params.sessionId);
  return apiGet<{ data: Cart }>(`/cart/?${qs}`, { auth: false, tenant: false }).then((r) => r.data);
}

export function addCartItem(
  params: { tenantId: string; storeId: string; customerId?: string; sessionId?: string; unitPrice: number },
  input: { productId: string; productVariantId?: string; quantity: number },
): Promise<Cart> {
  const qs = new URLSearchParams({
    tenantId: params.tenantId,
    storeId: params.storeId,
    unitPrice: String(params.unitPrice),
  });
  if (params.customerId) qs.set("customerId", params.customerId);
  if (params.sessionId) qs.set("sessionId", params.sessionId);
  return apiPost<{ data: Cart }>(`/cart/items?${qs}`, input, { auth: false, tenant: false }).then((r) => r.data);
}

export function updateCartItemQuantity(itemId: string, quantity: number): Promise<Cart> {
  return apiPatch<{ data: Cart }>(`/cart/items/${itemId}`, { quantity }, { auth: false, tenant: false }).then((r) => r.data);
}

export function removeCartItem(itemId: string): Promise<Cart> {
  return apiDelete<{ data: Cart }>(`/cart/items/${itemId}`, { auth: false, tenant: false }).then((r) => r.data);
}

export function applyCartCoupon(
  cartId: string,
  input: { couponCode: string; customerId: string },
): Promise<{ couponCode: string; discountAmount: string; cart: Cart }> {
  return apiPost<{ data: { couponCode: string; discountAmount: string; cart: Cart } }>(
    `/cart/${cartId}/coupon`,
    input,
    { auth: false, tenant: false },
  ).then((r) => r.data);
}

export function markCartAbandoned(cartId: string): Promise<void> {
  return apiPost<void>(`/cart/${cartId}/mark-abandoned`, undefined, { auth: false, tenant: false });
}

// ============================================================================
// Orders
// ============================================================================

export function createOrder(input: {
  tenantId: string;
  storeId: string;
  customerId: string;
  billingAddressId: string;
  shippingAddressId: string;
  items: OrderItemInput[];
  shippingAmount?: number;
  customerNote?: string;
  cartId?: string;
}): Promise<Order> {
  return apiPost<{ data: Order }>("/orders/", input, { auth: false, tenant: false }).then((r) => r.data);
}

export function getOrder(orderId: string): Promise<Order> {
  return apiGet<{ data: Order }>(`/orders/${orderId}`, { auth: false, tenant: false }).then((r) => r.data);
}

export function getOrderStatusHistory(orderId: string): Promise<OrderStatusEvent[]> {
  return apiGet<{ data: OrderStatusEvent[] }>(`/orders/${orderId}/history`, { auth: false, tenant: false }).then((r) => r.data);
}

/** Staff-only — requires a bearer token + tenant context, unlike everything else in this file. */
export function updateOrderStatus(orderId: string, status: OrderStatus, reason?: string): Promise<Order> {
  return apiPatch<{ data: Order }>(`/orders/${orderId}/status`, { status, reason }).then((r) => r.data);
}

// ============================================================================
// Payments (Razorpay)
// ============================================================================

export function createRazorpayOrder(input: { tenantId: string; storeId: string; orderId: string }): Promise<CreateRazorpayOrderResult> {
  return apiPost<{ data: CreateRazorpayOrderResult }>("/payments/razorpay/create-order", input, {
    auth: false,
    tenant: false,
  }).then((r) => r.data);
}

export function verifyRazorpayPayment(input: {
  razorpayOrderId: string;
  razorpayPaymentId: string;
  razorpaySignature: string;
}): Promise<{ verified: boolean; order: Order }> {
  return apiPost<{ data: { verified: boolean; order: Order } }>("/payments/razorpay/verify", input, {
    auth: false,
    tenant: false,
  }).then((r) => r.data);
}

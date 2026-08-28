import { apiGet, apiPost, apiPut, apiDelete } from "../client";
import { TENANT_ID, STORE_ID, assertStoreConfig } from "../config";

// order_status / payment_status / fulfillment_status are plain strings server-side
// (no enum validation on the Order model itself) — these are the values this UI uses.
export const ORDER_STATUSES = ["PENDING", "CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"] as const;
export const PAYMENT_STATUSES = ["PENDING", "PAID", "FAILED", "REFUNDED"] as const;
export const FULFILLMENT_STATUSES = ["PENDING", "PACKED", "SHIPPED", "DELIVERED"] as const;

export interface Order {
  id: string;
  tenant_id: string;
  store_id: string;
  customer_id: string;
  cart_id?: string | null;
  order_number: string;
  payment_id?: string | null;
  shipping_profile_id?: string | null;
  billing_address_id: string;
  shipping_address_id: string;
  order_status: string;
  payment_status: string;
  fulfillment_status: string;
  subtotal_amount: number;
  discount_amount: number;
  tax_amount: number;
  shipping_amount: number;
  total_amount: number;
  currency_code: string;
  customer_note?: string | null;
  placed_at: string;
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string;
  product_variant_id?: string | null;
  sku: string;
  product_name: string;
  variant_name?: string | null;
  hsn_code?: string | null;
  gst_rate: number;
  quantity: number;
  unit_price: number;
  discount_amount: number;
  tax_amount: number;
  shipping_amount: number;
  line_total: number;
}

export interface CreateOrderInput {
  customer_id: string;
  billing_address_id: string;
  shipping_address_id: string;
  subtotal_amount: number;
  total_amount: number;
  cart_id?: string;
  discount_amount?: number;
  tax_amount?: number;
  shipping_amount?: number;
  currency_code?: string;
  customer_note?: string;
}

const genOrderNumber = () => `ORD-${crypto.randomUUID().slice(0, 8).toUpperCase()}`;

export function createOrder(input: CreateOrderInput) {
  assertStoreConfig();
  return apiPost<Order>("/orders/", {
    tenant_id: TENANT_ID,
    store_id: STORE_ID,
    order_number: genOrderNumber(),
    order_status: "PENDING",
    payment_status: "PENDING",
    fulfillment_status: "PENDING",
    discount_amount: 0,
    tax_amount: 0,
    shipping_amount: 0,
    currency_code: "INR",
    ...input,
  });
}

// No customer-scoped list filter server-side — fetch all and filter client-side by customer_id.
export const listOrders = () => apiGet<Order[]>("/orders/");
export const getOrder = (orderId: string) => apiGet<Order>(`/orders/${orderId}`);
export const updateOrder = (
  orderId: string,
  data: Partial<Pick<Order, "order_status" | "payment_status" | "fulfillment_status" | "customer_note">>
) => apiPut<Order>(`/orders/${orderId}`, data);
export const deleteOrder = (orderId: string) => apiDelete<void>(`/orders/${orderId}`);

export interface CreateOrderItemInput {
  order_id: string;
  product_id: string;
  sku: string;
  product_name: string;
  quantity: number;
  unit_price: number;
  line_total: number;
  product_variant_id?: string;
  variant_name?: string;
  hsn_code?: string;
  gst_rate?: number;
  discount_amount?: number;
  tax_amount?: number;
  shipping_amount?: number;
}
export const createOrderItem = (input: CreateOrderItemInput) =>
  apiPost<OrderItem>("/order-items/", { gst_rate: 0, discount_amount: 0, tax_amount: 0, shipping_amount: 0, ...input });
export const listOrderItems = () => apiGet<OrderItem[]>("/order-items/");
export const getOrderItem = (orderItemId: string) => apiGet<OrderItem>(`/order-items/${orderItemId}`);

export interface OrderStatusUpdate {
  order_id: string;
  order_status: string;
  payment_status?: string;
  fulfillment_status?: string;
}
export interface OrderStatusResult {
  order_id: string;
  order_status: string;
  payment_status: string;
  fulfillment_status: string;
  message: string;
}
/** Real status-transition call — prefer over updateOrder() for status changes. */
export const updateOrderStatus = (input: OrderStatusUpdate) => apiPut<OrderStatusResult>("/order-status", input);

export interface OrderCancellation {
  id: string;
  order_id: string;
  requested_by?: string | null;
  cancellation_reason: string;
  cancellation_reason_description?: string | null;
  status?: string | null;
  approved_by?: string | null;
  approved_at?: string | null;
  created_at: string;
}
export const createOrderCancellation = (input: {
  order_id: string;
  cancellation_reason: string;
  cancellation_reason_description?: string;
  requested_by?: string;
}) => apiPost<OrderCancellation>("/order-cancellations/", input);
export const getOrderCancellationByOrder = (orderId: string) =>
  apiGet<OrderCancellation>(`/order-cancellations/by-order/${orderId}`);

export interface OrderReturn {
  id: string;
  order_id: string;
  return_reason: string;
  return_reason_description?: string | null;
  return_status?: "REQUESTED" | "APPROVED" | "REJECTED" | "RECEIVED" | "COMPLETED" | null;
  requested_at?: string | null;
  processed_at?: string | null;
  return_approved_by?: string | null;
}
export const createOrderReturn = (input: { order_id: string; return_reason: string; return_reason_description?: string }) =>
  apiPost<OrderReturn>("/order-returns/", input);
export const getOrderReturnByOrder = (orderId: string) => apiGet<OrderReturn>(`/order-returns/by-order/${orderId}`);

export interface OrderRefund {
  id: string;
  order_id: string;
  payment_refund_id?: string | null;
  refund_amount: number;
  refund_reason: string;
  refund_reference?: string | null;
  refund_status?: "PENDING" | "PROCESSING" | "SUCCESS" | "FAILED" | null;
  approved_by?: string | null;
  approved_at?: string | null;
  refunded_at?: string | null;
  created_at?: string;
}
export const createOrderRefund = (input: { order_id: string; refund_amount: number; refund_reason: string; refund_reference?: string }) =>
  apiPost<OrderRefund>("/order-refunds/", input);
export const listOrderRefundsByOrder = (orderId: string) => apiGet<OrderRefund[]>(`/order-refunds/by-order/${orderId}`);

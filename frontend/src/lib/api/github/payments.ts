import { apiGet, apiPost, apiPut, apiDelete } from "../client";
import { TENANT_ID, STORE_ID, assertStoreConfig } from "../config";

export interface Payment {
  id: string;
  tenant_id: string;
  store_id: string;
  entity_type: string;
  entity_id: string;
  payment_method_id: string;
  payment_reference_number?: string | null;
  amount: number;
  currency: string;
  payment_status: string;
  payment_date?: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaymentMethod {
  id: string;
  method_code: string;
  method_name: string;
  is_online: boolean;
  is_active: boolean;
  created_at: string;
}

export const listPayments = () => apiGet<Payment[]>("/payments/");
export const getPayment = (paymentId: string) => apiGet<Payment>(`/payments/${paymentId}`);

export const listPaymentMethods = () => apiGet<PaymentMethod[]>("/payment-methods/");

export interface RazorpayOrder {
  id: string;
  /** Paise, not rupees — razorpayService.createOrder() multiplies by 100 server-side. */
  amount: number;
  currency: string;
  [key: string]: unknown;
}

export interface CreatePaymentOrderResult {
  payment: Payment;
  razorpay_order: RazorpayOrder;
}

/** Combined flow: persists a Payment row + creates the matching Razorpay order in one call. */
export function createPaymentOrder(input: { entity_type: string; entity_id: string; payment_method_id: string; amount: number; receipt: string }) {
  assertStoreConfig();
  return apiPost<CreatePaymentOrderResult>("/payments/create-payment-order", {
    tenant_id: TENANT_ID,
    store_id: STORE_ID,
    ...input,
  });
}

export interface VerifyPaymentInput {
  razorpay_order_id: string;
  razorpay_payment_id: string;
  razorpay_signature: string;
}
/** Returns a bare boolean — razorpayService.verifySignature() returns True/False directly, no wrapper object. */
export const verifyPayment = (input: VerifyPaymentInput) => apiPost<boolean>("/payments/verify", input);

export const refundPayment = (input: { payment_id: string; amount?: number }) => apiPost<Record<string, unknown>>("/payments/refund", input);

export const createPaymentMethod = (input: { method_code: string; method_name: string; is_online?: boolean; is_active?: boolean }) =>
  apiPost<PaymentMethod>("/payment-methods/", { is_online: true, is_active: true, ...input });
export const getPaymentMethod = (paymentMethodId: string) => apiGet<PaymentMethod>(`/payment-methods/${paymentMethodId}`);
export const updatePaymentMethod = (paymentMethodId: string, data: Partial<Pick<PaymentMethod, "method_name" | "is_online" | "is_active">>) =>
  apiPut<PaymentMethod>(`/payment-methods/${paymentMethodId}`, data);
export const deletePaymentMethod = (paymentMethodId: string) => apiDelete<void>(`/payment-methods/${paymentMethodId}`);

// ---------------------------------------------------------------------------
// Payment Refunds — record-level, distinct from the /payments/refund gateway call above.
// ---------------------------------------------------------------------------

export interface PaymentRefund {
  id: string;
  payment_id: string;
  refund_reference?: string | null;
  refund_amount: number;
  refund_reason?: string | null;
  refund_status: string;
  refunded_at?: string | null;
  created_at: string;
}
export const createPaymentRefund = (input: { payment_id: string; refund_amount: number; refund_reason?: string }) =>
  apiPost<PaymentRefund>("/payment-refunds/", input);
export const listPaymentRefunds = () => apiGet<PaymentRefund[]>("/payment-refunds/");
export const getPaymentRefund = (refundId: string) => apiGet<PaymentRefund>(`/payment-refunds/${refundId}`);
export const updatePaymentRefund = (
  refundId: string,
  data: Partial<Pick<PaymentRefund, "refund_reference" | "refund_status" | "refunded_at">>
) => apiPut<PaymentRefund>(`/payment-refunds/${refundId}`, data);
export const deletePaymentRefund = (refundId: string) => apiDelete<void>(`/payment-refunds/${refundId}`);

// ---------------------------------------------------------------------------
// Payment Audit Logs
// ---------------------------------------------------------------------------

export interface PaymentAuditLog {
  id: string;
  payment_id: string;
  action_type: string;
  old_value?: Record<string, unknown> | null;
  new_value?: Record<string, unknown> | null;
  performed_by: string;
  created_at: string;
}
export const createPaymentAuditLog = (input: {
  payment_id: string;
  action_type: string;
  performed_by: string;
  old_value?: Record<string, unknown>;
  new_value?: Record<string, unknown>;
}) => apiPost<PaymentAuditLog>("/payment-audit-logs/", input);
export const listPaymentAuditLogs = () => apiGet<PaymentAuditLog[]>("/payment-audit-logs/");
export const getPaymentAuditLog = (auditId: string) => apiGet<PaymentAuditLog>(`/payment-audit-logs/${auditId}`);
export const updatePaymentAuditLog = (
  auditId: string,
  data: Partial<Pick<PaymentAuditLog, "action_type" | "old_value" | "new_value">>
) => apiPut<PaymentAuditLog>(`/payment-audit-logs/${auditId}`, data);
export const deletePaymentAuditLog = (auditId: string) => apiDelete<void>(`/payment-audit-logs/${auditId}`);

// ---------------------------------------------------------------------------
// Subscription Payments — platform SaaS billing, not storefront order payments.
// ---------------------------------------------------------------------------

export interface SubscriptionPayment {
  id: string;
  tenant_id: string;
  invoice_id: string;
  payment_reference?: string | null;
  payment_gateway: string;
  subscription_revenue: number;
  payment_status: string;
  paid_at?: string | null;
  created_at: string;
}
export function createSubscriptionPayment(input: {
  invoice_id: string;
  payment_gateway: string;
  subscription_revenue: number;
  payment_status: string;
  payment_reference?: string;
  paid_at?: string;
}) {
  assertStoreConfig();
  return apiPost<SubscriptionPayment>("/subscription-payments/", { tenant_id: TENANT_ID, ...input });
}
export const listSubscriptionPayments = () => apiGet<SubscriptionPayment[]>("/subscription-payments/");
export const getSubscriptionPayment = (paymentId: string) => apiGet<SubscriptionPayment>(`/subscription-payments/${paymentId}`);
export const updateSubscriptionPayment = (paymentId: string, data: Partial<Pick<SubscriptionPayment, "payment_status" | "paid_at">>) =>
  apiPut<SubscriptionPayment>(`/subscription-payments/${paymentId}`, data);
export const deleteSubscriptionPayment = (paymentId: string) => apiDelete<void>(`/subscription-payments/${paymentId}`);

// ---------------------------------------------------------------------------
// Gateway Settlements
// ---------------------------------------------------------------------------

export interface GatewaySettlement {
  id: string;
  settlement_reference: string;
  gateway_name: string;
  settlement_amount: number;
  settlement_date: string;
  settlement_status: string;
  created_at: string;
}
export const createGatewaySettlement = (input: {
  settlement_reference: string;
  gateway_name: string;
  settlement_amount: number;
  settlement_date: string;
  settlement_status?: string;
}) => apiPost<GatewaySettlement>("/gateway-settlements/", { settlement_status: "PENDING", ...input });
export const listGatewaySettlements = () => apiGet<GatewaySettlement[]>("/gateway-settlements/");
export const getGatewaySettlement = (settlementId: string) => apiGet<GatewaySettlement>(`/gateway-settlements/${settlementId}`);
export const updateGatewaySettlement = (settlementId: string, data: { settlement_status: string }) =>
  apiPut<GatewaySettlement>(`/gateway-settlements/${settlementId}`, data);
export const deleteGatewaySettlement = (settlementId: string) => apiDelete<void>(`/gateway-settlements/${settlementId}`);

export interface GatewaySettlementItem {
  id: string;
  settlement_id: string;
  payment_id: string;
  settlement_amount: number;
  fee_amount: number;
  tax_amount: number;
  created_at: string;
}
export const createGatewaySettlementItem = (input: {
  settlement_id: string;
  payment_id: string;
  settlement_amount: number;
  fee_amount?: number;
  tax_amount?: number;
}) => apiPost<GatewaySettlementItem>("/gateway-settlement-items/", { fee_amount: 0, tax_amount: 0, ...input });
export const listGatewaySettlementItems = () => apiGet<GatewaySettlementItem[]>("/gateway-settlement-items/");
export const getGatewaySettlementItem = (itemId: string) => apiGet<GatewaySettlementItem>(`/gateway-settlement-items/${itemId}`);
export const updateGatewaySettlementItem = (
  itemId: string,
  data: Partial<Pick<GatewaySettlementItem, "settlement_amount" | "fee_amount" | "tax_amount">>
) => apiPut<GatewaySettlementItem>(`/gateway-settlement-items/${itemId}`, data);
export const deleteGatewaySettlementItem = (itemId: string) => apiDelete<void>(`/gateway-settlement-items/${itemId}`);

// ---------------------------------------------------------------------------
// Gateway Webhook Events — audit-trail style, no DELETE route.
// ---------------------------------------------------------------------------

export interface GatewayWebhookEvent {
  id: string;
  gateway_name: string;
  event_type: string;
  event_id: string;
  payload: Record<string, unknown>;
  processed: boolean;
  processed_at?: string | null;
  received_at: string;
}
export const createGatewayWebhookEvent = (input: { gateway_name: string; event_type: string; event_id: string; payload: Record<string, unknown> }) =>
  apiPost<GatewayWebhookEvent>("/gateway-webhook-events/", input);
export const listGatewayWebhookEvents = () => apiGet<GatewayWebhookEvent[]>("/gateway-webhook-events/");
export const getGatewayWebhookEvent = (eventId: string) => apiGet<GatewayWebhookEvent>(`/gateway-webhook-events/${eventId}`);
export const updateGatewayWebhookEvent = (eventId: string, data: { processed?: boolean; processed_at?: string }) =>
  apiPut<GatewayWebhookEvent>(`/gateway-webhook-events/${eventId}`, data);

// ---------------------------------------------------------------------------
// Payment Reconciliation
// ---------------------------------------------------------------------------

export interface PaymentReconciliationBatch {
  id: string;
  batch_number: string;
  reconciliation_date: string;
  total_payments: number;
  total_amount: number;
  status: string;
  created_at: string;
}
export const createReconciliationBatch = (input: {
  batch_number: string;
  reconciliation_date: string;
  total_payments?: number;
  total_amount?: number;
  status?: string;
}) => apiPost<PaymentReconciliationBatch>("/payment-reconciliation-batches/", { total_payments: 0, total_amount: 0, status: "PENDING", ...input });
export const listReconciliationBatches = () => apiGet<PaymentReconciliationBatch[]>("/payment-reconciliation-batches/");
export const getReconciliationBatch = (batchId: string) => apiGet<PaymentReconciliationBatch>(`/payment-reconciliation-batches/${batchId}`);
export const updateReconciliationBatch = (
  batchId: string,
  data: Partial<Pick<PaymentReconciliationBatch, "total_payments" | "total_amount" | "status">>
) => apiPut<PaymentReconciliationBatch>(`/payment-reconciliation-batches/${batchId}`, data);
export const deleteReconciliationBatch = (batchId: string) => apiDelete<void>(`/payment-reconciliation-batches/${batchId}`);

export interface PaymentReconciliationItem {
  id: string;
  batch_id: string;
  payment_id: string;
  gateway_payment_id?: string | null;
  reconciliation_status: string;
  notes?: string | null;
  created_at: string;
}
export const createReconciliationItem = (input: {
  batch_id: string;
  payment_id: string;
  gateway_payment_id?: string;
  reconciliation_status?: string;
  notes?: string;
}) => apiPost<PaymentReconciliationItem>("/payment-reconciliation-items/", { reconciliation_status: "MATCHED", ...input });
export const listReconciliationItems = () => apiGet<PaymentReconciliationItem[]>("/payment-reconciliation-items/");
export const getReconciliationItem = (itemId: string) => apiGet<PaymentReconciliationItem>(`/payment-reconciliation-items/${itemId}`);
export const updateReconciliationItem = (itemId: string, data: Partial<Pick<PaymentReconciliationItem, "reconciliation_status" | "notes">>) =>
  apiPut<PaymentReconciliationItem>(`/payment-reconciliation-items/${itemId}`, data);
export const deleteReconciliationItem = (itemId: string) => apiDelete<void>(`/payment-reconciliation-items/${itemId}`);

// ---------------------------------------------------------------------------
// Revenue Summary
// ---------------------------------------------------------------------------

export interface RevenueSummary {
  id: string;
  tenant_id: string;
  report_month: string;
  subscription_revenue: number;
  commission_revenue: number;
  total_revenue: number;
  created_at: string;
}
export function createRevenueSummary(input: { report_month: string; subscription_revenue?: number; commission_revenue?: number; total_revenue?: number }) {
  assertStoreConfig();
  return apiPost<RevenueSummary>("/revenue-summary/", { subscription_revenue: 0, commission_revenue: 0, total_revenue: 0, tenant_id: TENANT_ID, ...input });
}
export const listRevenueSummaries = () => apiGet<RevenueSummary[]>("/revenue-summary/");
export const getRevenueSummary = (revenueId: string) => apiGet<RevenueSummary>(`/revenue-summary/${revenueId}`);
export const updateRevenueSummary = (
  revenueId: string,
  data: Partial<Pick<RevenueSummary, "subscription_revenue" | "commission_revenue" | "total_revenue">>
) => apiPut<RevenueSummary>(`/revenue-summary/${revenueId}`, data);
export const deleteRevenueSummary = (revenueId: string) => apiDelete<void>(`/revenue-summary/${revenueId}`);

// ---------------------------------------------------------------------------
// Commission — stateless calculator, does not persist anything.
// ---------------------------------------------------------------------------

export interface CommissionResult {
  order_id: string;
  order_amount: number;
  commission_percentage: number;
  commission_amount: number;
  seller_amount: number;
  message: string;
}
export const calculateCommission = (input: { order_id: string; order_amount: number; commission_percentage: number }) =>
  apiPost<CommissionResult>("/commission/calculate", input);

// ---------------------------------------------------------------------------
// Seller Payouts
// ---------------------------------------------------------------------------

export interface SellerPayout {
  id: string;
  tenant_id: string;
  payment_id: string;
  payout_reference?: string | null;
  gross_amount: number;
  gateway_fee: number;
  gateway_tax: number;
  platform_commission: number;
  net_payout_amount: number;
  payout_status: string;
  payout_date?: string | null;
  created_at: string;
}
export function createSellerPayout(input: {
  payment_id: string;
  gross_amount: number;
  net_payout_amount: number;
  payout_reference?: string;
  gateway_fee?: number;
  gateway_tax?: number;
  platform_commission?: number;
  payout_status?: string;
  payout_date?: string;
}) {
  assertStoreConfig();
  return apiPost<SellerPayout>("/seller-payouts/", {
    gateway_fee: 0,
    gateway_tax: 0,
    platform_commission: 0,
    payout_status: "PENDING",
    tenant_id: TENANT_ID,
    ...input,
  });
}
export const listSellerPayouts = () => apiGet<SellerPayout[]>("/seller-payouts/");
export const getSellerPayout = (payoutId: string) => apiGet<SellerPayout>(`/seller-payouts/${payoutId}`);
export const updateSellerPayout = (payoutId: string, data: Partial<Pick<SellerPayout, "payout_status" | "payout_date">>) =>
  apiPut<SellerPayout>(`/seller-payouts/${payoutId}`, data);
export const deleteSellerPayout = (payoutId: string) => apiDelete<void>(`/seller-payouts/${payoutId}`);

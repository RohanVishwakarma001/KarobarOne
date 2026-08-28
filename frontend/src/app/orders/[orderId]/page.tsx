"use client";

import Link from "next/link";
import { use, useCallback, useEffect, useState } from "react";
import { toast } from "sonner";
import { ChevronLeft, Loader2, PackageOpen, Truck, XCircle, RotateCcw } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import {
  ApiError,
  type Order,
  type OrderItem,
  type OrderCancellation,
  type OrderReturn,
  type Shipment,
  getOrder,
  listOrderItems,
  getOrderCancellationByOrder,
  getOrderReturnByOrder,
  createOrderCancellation,
  createOrderReturn,
  updateOrderStatus,
  listShipments,
  trackShipment,
} from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
const dateFmt = (iso: string) => new Date(iso).toLocaleString("en-IN", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });

const statusClass = (s: string) =>
  s === "DELIVERED" ? "bg-green-50 text-green-700" : s === "CANCELLED" ? "bg-red-50 text-red-700" : s === "SHIPPED" ? "bg-blue-50 text-blue-700" : "bg-amber-50 text-amber-700";

const CANCELLABLE_STATUSES = ["PENDING", "CONFIRMED", "PROCESSING"];
const RETURNABLE_STATUSES = ["DELIVERED"];

export default function OrderDetailPage({ params }: { params: Promise<{ orderId: string }> }) {
  const { orderId } = use(params);
  const [order, setOrder] = useState<Order | null>(null);
  const [items, setItems] = useState<OrderItem[]>([]);
  const [shipment, setShipment] = useState<Shipment | null>(null);
  const [tracking, setTracking] = useState<Record<string, unknown> | null>(null);
  const [cancellation, setCancellation] = useState<OrderCancellation | null>(null);
  const [orderReturn, setOrderReturn] = useState<OrderReturn | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [showCancelForm, setShowCancelForm] = useState(false);
  const [cancelReason, setCancelReason] = useState("");
  const [showReturnForm, setShowReturnForm] = useState(false);
  const [returnReason, setReturnReason] = useState("");
  const [actionBusy, setActionBusy] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [o, allItems, allShipments] = await Promise.all([getOrder(orderId), listOrderItems(), listShipments()]);
      setOrder(o);
      setItems(allItems.filter((i) => i.order_id === orderId));
      const relatedShipment = allShipments.find((s) => s.order_id === orderId) ?? null;
      setShipment(relatedShipment);

      try {
        setCancellation(await getOrderCancellationByOrder(orderId));
      } catch (e) {
        if (!(e instanceof ApiError && e.status === 404)) throw e;
      }
      try {
        setOrderReturn(await getOrderReturnByOrder(orderId));
      } catch (e) {
        if (!(e instanceof ApiError && e.status === 404)) throw e;
      }

      if (relatedShipment?.tracking_number) {
        try {
          setTracking(await trackShipment(relatedShipment.tracking_number));
        } catch {
          // tracking is best-effort; leave null on failure
        }
      }
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not load this order.");
    } finally {
      setLoading(false);
    }
  }, [orderId]);

  useEffect(() => {
    load();
  }, [load]);

  async function handleCancel(e: React.FormEvent) {
    e.preventDefault();
    if (!cancelReason.trim()) {
      toast.error("Enter a cancellation reason.");
      return;
    }
    setActionBusy(true);
    try {
      const rec = await createOrderCancellation({ order_id: orderId, cancellation_reason: cancelReason.trim() });
      setCancellation(rec);
      await updateOrderStatus({ order_id: orderId, order_status: "CANCELLED" });
      setOrder((prev) => (prev ? { ...prev, order_status: "CANCELLED" } : prev));
      setShowCancelForm(false);
      toast.success("Order cancellation requested.");
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not cancel this order.");
    } finally {
      setActionBusy(false);
    }
  }

  async function handleReturn(e: React.FormEvent) {
    e.preventDefault();
    if (!returnReason.trim()) {
      toast.error("Enter a return reason.");
      return;
    }
    setActionBusy(true);
    try {
      const rec = await createOrderReturn({ order_id: orderId, return_reason: returnReason.trim() });
      setOrderReturn(rec);
      setShowReturnForm(false);
      toast.success("Return requested.");
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not request a return.");
    } finally {
      setActionBusy(false);
    }
  }

  return (
    <CommerceShell title={order ? order.order_number : "Order"} eyebrow="Orders & Payments">
      <div className="mx-auto max-w-7xl px-6">
        <Link href="/orders" className="mb-5 inline-flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-[#5b4ef9]">
          <ChevronLeft className="h-4 w-4" /> Back to orders
        </Link>

        {loading && (
          <div className="flex items-center justify-center gap-2 rounded-2xl border border-gray-200 bg-white px-6 py-16 text-sm text-gray-500">
            <Loader2 className="h-4 w-4 animate-spin" /> Loading order…
          </div>
        )}

        {!loading && error && <div className="rounded-2xl border border-gray-200 bg-white px-6 py-16 text-center font-medium text-red-600">{error}</div>}

        {!loading && !error && order && (
          <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
            <div className="space-y-6">
              <section className="rounded-2xl border border-gray-200 bg-white p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <h2 className="font-semibold">{order.order_number}</h2>
                    <p className="mt-1 text-sm text-gray-500">Placed {dateFmt(order.placed_at)}</p>
                  </div>
                  <div className="flex gap-2">
                    <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(order.order_status)}`}>{order.order_status}</span>
                    <span className="rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700">{order.payment_status}</span>
                  </div>
                </div>
              </section>

              <section className="rounded-2xl border border-gray-200 bg-white">
                <div className="border-b border-gray-200 px-5 py-4">
                  <h2 className="font-semibold">Items</h2>
                </div>
                {items.length === 0 ? (
                  <div className="px-5 py-10 text-center text-sm text-gray-400">
                    <PackageOpen className="mx-auto mb-2 h-6 w-6 text-gray-300" /> No line items recorded.
                  </div>
                ) : (
                  items.map((item) => (
                    <div key={item.id} className="flex items-center justify-between gap-4 border-b border-gray-100 px-5 py-4 last:border-0">
                      <div>
                        <p className="font-medium">{item.product_name}</p>
                        <p className="mt-1 text-sm text-gray-500">
                          {item.sku} · Qty {item.quantity} · {money(item.unit_price)} each
                        </p>
                      </div>
                      <p className="font-semibold">{money(item.line_total)}</p>
                    </div>
                  ))
                )}
              </section>

              {shipment && (
                <section className="rounded-2xl border border-gray-200 bg-white p-5">
                  <div className="flex items-center gap-3">
                    <span className="rounded-lg bg-[#5b4ef9]/10 p-2 text-[#5b4ef9]">
                      <Truck className="h-5 w-5" />
                    </span>
                    <div>
                      <h2 className="font-semibold">Shipment</h2>
                      <p className="text-sm text-gray-500">{shipment.shipment_status}</p>
                    </div>
                  </div>
                  <div className="mt-4 space-y-1 text-sm text-gray-600">
                    {shipment.tracking_number && <p>Tracking number: {shipment.tracking_number}</p>}
                    {shipment.tracking_url && (
                      <a href={shipment.tracking_url} target="_blank" rel="noreferrer" className="text-[#5b4ef9] hover:underline">
                        Track on carrier site
                      </a>
                    )}
                    {tracking && <p className="pt-2 text-xs text-gray-500">Latest status: {String(tracking.current_status ?? "Unavailable")}</p>}
                  </div>
                </section>
              )}

              {(order.order_status === "CANCELLED" && cancellation) && (
                <section className="rounded-2xl border border-red-100 bg-red-50/40 p-5">
                  <h2 className="font-semibold text-red-700">Cancellation</h2>
                  <p className="mt-1 text-sm text-red-700/80">{cancellation.cancellation_reason}</p>
                  {cancellation.status && <p className="mt-1 text-xs text-red-700/60">Status: {cancellation.status}</p>}
                </section>
              )}

              {orderReturn && (
                <section className="rounded-2xl border border-amber-100 bg-amber-50/40 p-5">
                  <h2 className="font-semibold text-amber-700">Return</h2>
                  <p className="mt-1 text-sm text-amber-700/80">{orderReturn.return_reason}</p>
                  {orderReturn.return_status && <p className="mt-1 text-xs text-amber-700/60">Status: {orderReturn.return_status}</p>}
                </section>
              )}
            </div>

            <aside className="h-fit space-y-4 rounded-2xl border border-gray-200 bg-white p-5 lg:sticky lg:top-28">
              <h2 className="font-semibold">Order total</h2>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span>{money(order.subtotal_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Discount</span>
                  <span>-{money(order.discount_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Shipping</span>
                  <span>{order.shipping_amount ? money(order.shipping_amount) : "Free"}</span>
                </div>
                <div className="flex justify-between">
                  <span>Tax</span>
                  <span>{money(order.tax_amount)}</span>
                </div>
                <div className="border-t border-gray-100 pt-2">
                  <div className="flex justify-between text-base font-semibold text-gray-900">
                    <span>Total</span>
                    <span>{money(order.total_amount)}</span>
                  </div>
                </div>
              </div>

              {CANCELLABLE_STATUSES.includes(order.order_status) && !cancellation && (
                <div className="border-t border-gray-100 pt-4">
                  {!showCancelForm ? (
                    <button
                      onClick={() => setShowCancelForm(true)}
                      className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-red-200 px-4 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50"
                    >
                      <XCircle className="h-4 w-4" /> Cancel order
                    </button>
                  ) : (
                    <form onSubmit={handleCancel} className="space-y-2">
                      <textarea
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-[#5b4ef9]"
                        rows={2}
                        placeholder="Why are you cancelling?"
                        value={cancelReason}
                        onChange={(e) => setCancelReason(e.target.value)}
                      />
                      <div className="flex gap-2">
                        <button disabled={actionBusy} type="submit" className="flex-1 rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
                          {actionBusy ? "Cancelling…" : "Confirm cancellation"}
                        </button>
                        <button type="button" onClick={() => setShowCancelForm(false)} className="rounded-lg px-4 py-2 text-sm text-gray-500">
                          Back
                        </button>
                      </div>
                    </form>
                  )}
                </div>
              )}

              {RETURNABLE_STATUSES.includes(order.order_status) && !orderReturn && (
                <div className="border-t border-gray-100 pt-4">
                  {!showReturnForm ? (
                    <button
                      onClick={() => setShowReturnForm(true)}
                      className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:border-[#5b4ef9]/40 hover:text-[#5b4ef9]"
                    >
                      <RotateCcw className="h-4 w-4" /> Request return
                    </button>
                  ) : (
                    <form onSubmit={handleReturn} className="space-y-2">
                      <textarea
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-[#5b4ef9]"
                        rows={2}
                        placeholder="Why are you returning this order?"
                        value={returnReason}
                        onChange={(e) => setReturnReason(e.target.value)}
                      />
                      <div className="flex gap-2">
                        <button disabled={actionBusy} type="submit" className="flex-1 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
                          {actionBusy ? "Submitting…" : "Submit return"}
                        </button>
                        <button type="button" onClick={() => setShowReturnForm(false)} className="rounded-lg px-4 py-2 text-sm text-gray-500">
                          Back
                        </button>
                      </div>
                    </form>
                  )}
                </div>
              )}
            </aside>
          </div>
        )}
      </div>
    </CommerceShell>
  );
}

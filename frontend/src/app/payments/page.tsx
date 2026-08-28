"use client";

import { useEffect, useState } from "react";
import { CreditCard, CheckCircle2, RotateCcw, Loader2 } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import { useCustomerSession } from "@/hooks/use-customer-session";
import { ApiError, type Order, type Payment, listOrders, listPayments } from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
const dateFmt = (iso?: string | null) => (iso ? new Date(iso).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" }) : "—");

const statusClass = (s: string) => (s === "PAID" ? "bg-green-50 text-green-700" : s === "REFUNDED" ? "bg-gray-100 text-gray-600" : s === "FAILED" ? "bg-red-50 text-red-700" : "bg-amber-50 text-amber-700");

export default function PaymentsPage() {
  const { customerId, ready } = useCustomerSession();
  const [payments, setPayments] = useState<Payment[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ready || !customerId) return;
    setLoading(true);
    Promise.all([listPayments(), listOrders()])
      .then(([allPayments, allOrders]) => {
        const myOrders = allOrders.filter((o) => o.customer_id === customerId);
        const myOrderIds = new Set(myOrders.map((o) => o.id));
        setOrders(myOrders);
        setPayments(
          allPayments
            .filter((p) => p.entity_type === "ORDER" && myOrderIds.has(p.entity_id))
            .sort((a, b) => b.created_at.localeCompare(a.created_at))
        );
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load payments."))
      .finally(() => setLoading(false));
  }, [customerId, ready]);

  const orderNumber = (orderId: string) => orders.find((o) => o.id === orderId)?.order_number ?? orderId.slice(0, 8);

  const totalPaid = payments.filter((p) => p.payment_status === "PAID").reduce((s, p) => s + p.amount, 0);
  const totalRefunded = payments.filter((p) => p.payment_status === "REFUNDED").reduce((s, p) => s + p.amount, 0);
  const paidCount = payments.filter((p) => p.payment_status === "PAID").length;
  const refundedCount = payments.filter((p) => p.payment_status === "REFUNDED").length;

  return (
    <CommerceShell title="Payments" eyebrow="Orders & Payments">
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border border-gray-200 bg-white p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-500">Total paid</p>
              <CheckCircle2 className="h-5 w-5 text-green-600" />
            </div>
            <p className="mt-3 text-2xl font-semibold">{money(totalPaid)}</p>
            <p className="mt-1 text-xs text-gray-500">{paidCount} successful payment{paidCount === 1 ? "" : "s"}</p>
          </div>
          <div className="rounded-2xl border border-gray-200 bg-white p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-500">Refunded</p>
              <RotateCcw className="h-5 w-5 text-gray-500" />
            </div>
            <p className="mt-3 text-2xl font-semibold">{money(totalRefunded)}</p>
            <p className="mt-1 text-xs text-gray-500">{refundedCount} refunded transaction{refundedCount === 1 ? "" : "s"}</p>
          </div>
        </div>

        <section className="mt-6 overflow-hidden rounded-2xl border border-gray-200 bg-white">
          <div className="border-b border-gray-200 px-5 py-4">
            <h2 className="font-semibold">Payment history</h2>
            <p className="mt-1 text-sm text-gray-500">Transactions connected to your orders.</p>
          </div>

          {loading && (
            <div className="flex items-center justify-center gap-2 px-6 py-16 text-sm text-gray-500">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading payments…
            </div>
          )}
          {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
          {!loading && !error && payments.length === 0 && (
            <div className="px-6 py-16 text-center">
              <CreditCard className="mx-auto h-8 w-8 text-gray-300" />
              <p className="mt-4 font-medium">No payments yet</p>
            </div>
          )}

          <div className="divide-y divide-gray-100">
            {payments.map((p) => (
              <div key={p.id} className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#5b4ef9]/10 text-[#5b4ef9]">
                    <CreditCard className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-medium">{p.payment_reference_number ?? p.id.slice(0, 8)}</p>
                    <p className="mt-1 text-sm text-gray-500">
                      {orderNumber(p.entity_id)} · {dateFmt(p.payment_date ?? p.created_at)}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-semibold">{money(p.amount)}</p>
                  <span className={`mt-1 inline-block rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(p.payment_status)}`}>{p.payment_status}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </CommerceShell>
  );
}

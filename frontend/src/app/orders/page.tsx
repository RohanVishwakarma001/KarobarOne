"use client";

import Link from "next/link";
import { Search, ChevronRight, PackageOpen, Loader2 } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import { useState, useEffect } from "react";
import { useCustomerSession } from "@/hooks/use-customer-session";
import { ApiError, type Order, listOrders } from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
const dateFmt = (iso: string) => new Date(iso).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });

const statusClass = (s: string) =>
  s === "DELIVERED"
    ? "bg-green-50 text-green-700"
    : s === "CANCELLED"
    ? "bg-red-50 text-red-700"
    : s === "SHIPPED"
    ? "bg-blue-50 text-blue-700"
    : "bg-amber-50 text-amber-700";

export default function OrdersPage() {
  const { customerId, ready } = useCustomerSession();
  const [query, setQuery] = useState("");
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ready || !customerId) return;
    setLoading(true);
    listOrders()
      .then((all) => setOrders(all.filter((o) => o.customer_id === customerId).sort((a, b) => b.placed_at.localeCompare(a.placed_at))))
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load orders."))
      .finally(() => setLoading(false));
  }, [customerId, ready]);

  const filtered = orders.filter(
    (o) => o.order_number.toLowerCase().includes(query.toLowerCase()) || o.order_status.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <CommerceShell title="Orders" eyebrow="Orders & Payments">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-gray-500">Track and manage all your orders.</p>
          <div className="relative w-full sm:w-72">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search order or status"
              className="w-full rounded-lg border border-gray-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-[#5b4ef9]"
            />
          </div>
        </div>

        <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white">
          {loading && (
            <div className="flex items-center justify-center gap-2 px-6 py-16 text-sm text-gray-500">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading your orders…
            </div>
          )}
          {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
          {!loading && !error && (
            <>
              <div className="hidden overflow-x-auto md:block">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      {["Order", "Date", "Amount", "Status", "Payment", "Action"].map((h) => (
                        <th key={h} className="border-b border-gray-200 px-5 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((o) => (
                      <tr key={o.id} className="hover:bg-gray-50/70">
                        <td className="px-5 py-4 font-medium">{o.order_number}</td>
                        <td className="px-5 py-4 text-sm text-gray-600">{dateFmt(o.placed_at)}</td>
                        <td className="px-5 py-4 text-sm font-medium">{money(o.total_amount)}</td>
                        <td className="px-5 py-4">
                          <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(o.order_status)}`}>{o.order_status}</span>
                        </td>
                        <td className="px-5 py-4 text-sm text-gray-600">{o.payment_status}</td>
                        <td className="px-5 py-4">
                          <Link href={`/orders/${o.id}`} className="inline-flex items-center gap-1 text-sm font-medium text-[#5b4ef9]">
                            View <ChevronRight className="h-4 w-4" />
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="divide-y divide-gray-100 md:hidden">
                {filtered.map((o) => (
                  <Link href={`/orders/${o.id}`} key={o.id} className="block p-5">
                    <div className="flex justify-between gap-3">
                      <div>
                        <p className="font-medium">{o.order_number}</p>
                        <p className="mt-1 text-sm text-gray-500">{dateFmt(o.placed_at)}</p>
                      </div>
                      <span className={`h-fit rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(o.order_status)}`}>{o.order_status}</span>
                    </div>
                    <div className="mt-4 flex items-center justify-between">
                      <span className="font-semibold">{money(o.total_amount)}</span>
                      <span className="text-sm font-medium text-[#5b4ef9]">View order</span>
                    </div>
                  </Link>
                ))}
              </div>
              {!filtered.length && (
                <div className="px-6 py-16 text-center">
                  <PackageOpen className="mx-auto h-8 w-8 text-gray-300" />
                  <p className="mt-4 font-medium">No orders found</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </CommerceShell>
  );
}

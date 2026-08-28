"use client";

import Link from "next/link";
import { useState } from "react";
import { Search, ChevronRight, CalendarClock, Loader2, Plus } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import { useBookings } from "@/hooks/use-bookings";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
const dateFmt = (iso: string) => new Date(iso).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });

const statusClass = (s: string) =>
  s === "COMPLETED"
    ? "bg-green-50 text-green-700"
    : s === "CANCELLED" || s === "REJECTED" || s === "NO_SHOW"
    ? "bg-red-50 text-red-700"
    : s === "CONFIRMED" || s === "APPROVED"
    ? "bg-blue-50 text-blue-700"
    : s === "REFUNDED"
    ? "bg-gray-100 text-gray-700"
    : "bg-amber-50 text-amber-700";

export default function BookingsPage() {
  const { bookings, loading, error } = useBookings();
  const [query, setQuery] = useState("");

  const filtered = bookings.filter(
    (b) => b.booking_number.toLowerCase().includes(query.toLowerCase()) || b.booking_status.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <CommerceShell title="Bookings" eyebrow="Orders & Payments">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-gray-500">Your service bookings and appointments.</p>
          <div className="flex w-full gap-3 sm:w-auto">
            <div className="relative w-full sm:w-72">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search booking or status"
                className="w-full rounded-lg border border-gray-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-[#5b4ef9]"
              />
            </div>
            <Link
              href="/bookings/new"
              className="inline-flex shrink-0 items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2.5 text-sm font-medium text-white hover:bg-[#4a3ee0]"
            >
              <Plus className="h-4 w-4" /> New booking
            </Link>
          </div>
        </div>

        <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white">
          {loading && (
            <div className="flex items-center justify-center gap-2 px-6 py-16 text-sm text-gray-500">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading your bookings…
            </div>
          )}
          {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
          {!loading && !error && (
            <>
              <div className="hidden overflow-x-auto md:block">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      {["Booking", "Date", "Amount", "Status", "Payment", "Action"].map((h) => (
                        <th key={h} className="border-b border-gray-200 px-5 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((b) => (
                      <tr key={b.id} className="hover:bg-gray-50/70">
                        <td className="px-5 py-4 font-medium">{b.booking_number}</td>
                        <td className="px-5 py-4 text-sm text-gray-600">
                          {b.booking_date} · {b.start_time.slice(0, 5)}–{b.end_time.slice(0, 5)}
                        </td>
                        <td className="px-5 py-4 text-sm font-medium">{money(b.total_amount)}</td>
                        <td className="px-5 py-4">
                          <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(b.booking_status)}`}>{b.booking_status}</span>
                        </td>
                        <td className="px-5 py-4 text-sm text-gray-600">{b.payment_status}</td>
                        <td className="px-5 py-4">
                          <Link href={`/bookings/${b.id}`} className="inline-flex items-center gap-1 text-sm font-medium text-[#5b4ef9]">
                            View <ChevronRight className="h-4 w-4" />
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="divide-y divide-gray-100 md:hidden">
                {filtered.map((b) => (
                  <Link href={`/bookings/${b.id}`} key={b.id} className="block p-5">
                    <div className="flex justify-between gap-3">
                      <div>
                        <p className="font-medium">{b.booking_number}</p>
                        <p className="mt-1 text-sm text-gray-500">
                          {dateFmt(b.booking_date)} · {b.start_time.slice(0, 5)}–{b.end_time.slice(0, 5)}
                        </p>
                      </div>
                      <span className={`h-fit rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(b.booking_status)}`}>{b.booking_status}</span>
                    </div>
                    <div className="mt-4 flex items-center justify-between">
                      <span className="font-semibold">{money(b.total_amount)}</span>
                      <span className="text-sm font-medium text-[#5b4ef9]">View booking</span>
                    </div>
                  </Link>
                ))}
              </div>
              {!filtered.length && (
                <div className="px-6 py-16 text-center">
                  <CalendarClock className="mx-auto h-8 w-8 text-gray-300" />
                  <p className="mt-4 font-medium">No bookings found</p>
                  <Link href="/bookings/new" className="mt-3 inline-flex items-center gap-1 text-sm font-medium text-[#5b4ef9]">
                    Make your first booking <ChevronRight className="h-4 w-4" />
                  </Link>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </CommerceShell>
  );
}

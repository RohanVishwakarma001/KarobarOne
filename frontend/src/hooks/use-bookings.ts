"use client";

import { useCallback, useEffect, useState } from "react";
import { ApiError, type Booking, listBookings } from "@/lib/api/github";
import { useCustomerSession } from "./use-customer-session";

/** No customer-scoped filter server-side — fetch all and filter client-side, same pattern as useCart/useWishlist. */
export function useBookings() {
  const { customerId, ready } = useCustomerSession();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!ready || !customerId) return;
    setLoading(true);
    setError(null);
    try {
      const all = await listBookings();
      setBookings(all.filter((b) => b.customer_id === customerId).sort((a, b) => (b.booked_at ?? b.created_at ?? "").localeCompare(a.booked_at ?? a.created_at ?? "")));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not load your bookings.");
    } finally {
      setLoading(false);
    }
  }, [customerId, ready]);

  useEffect(() => {
    load();
  }, [load]);

  return { customerId, ready, bookings, loading, error, refresh: load };
}

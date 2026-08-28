"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "karobar_customer_id";

function generateId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID();
  return `guest-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

/**
 * Stand-in identity until real platform auth is wired up (the /login page is
 * currently a mock with no backend call). Persists a per-browser guest customer
 * id in localStorage so cart/orders/wishlist calls have someone to attach to.
 * Swap this out once real session-based auth lands.
 */
export function useCustomerSession() {
  const [customerId, setCustomerId] = useState<string | null>(null);

  useEffect(() => {
    let id = window.localStorage.getItem(STORAGE_KEY);
    if (!id) {
      id = generateId();
      window.localStorage.setItem(STORAGE_KEY, id);
    }
    setCustomerId(id);
  }, []);

  return { customerId, ready: customerId !== null };
}

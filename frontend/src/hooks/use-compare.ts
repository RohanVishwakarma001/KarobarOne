"use client";

import { useCallback, useEffect, useState } from "react";
import {
  ApiError,
  type ProductCompareList,
  type ProductCompareItem,
  addCompareItem,
  createCompareList,
  listCompareLists,
  listCompareItems,
  removeCompareItem,
} from "@/lib/api/github";
import { useCustomerSession } from "./use-customer-session";

const COMPARE_LIST_ID_KEY = "karobar_compare_list_id";

/** No by-customer filter server-side — cache the compareListId locally, same pattern as useWishlist. */
export function useCompare() {
  const { customerId, ready } = useCustomerSession();
  const [compareList, setCompareList] = useState<ProductCompareList | null>(null);
  const [items, setItems] = useState<ProductCompareItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!ready || !customerId) return;
    setLoading(true);
    setError(null);
    try {
      let active: ProductCompareList | null = null;
      const cachedId = window.localStorage.getItem(COMPARE_LIST_ID_KEY);
      if (cachedId) {
        const all = await listCompareLists();
        active = all.find((l) => l.id === cachedId) ?? null;
      }
      if (!active) {
        active = await createCompareList(customerId);
        window.localStorage.setItem(COMPARE_LIST_ID_KEY, active.id);
      }
      setCompareList(active);
      const allItems = await listCompareItems();
      setItems(allItems.filter((i) => i.compare_list_id === active!.id));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not load your compare list.");
    } finally {
      setLoading(false);
    }
  }, [customerId, ready]);

  useEffect(() => {
    load();
  }, [load]);

  const addItem = useCallback(
    async (productId: string) => {
      if (!compareList) return;
      const item = await addCompareItem({ compare_list_id: compareList.id, product_id: productId });
      setItems((prev) => [...prev, item]);
    },
    [compareList]
  );

  const removeItem = useCallback(async (compareItemId: string) => {
    await removeCompareItem(compareItemId);
    setItems((prev) => prev.filter((i) => i.id !== compareItemId));
  }, []);

  return { customerId, compareList, items, loading, error, addItem, removeItem, refresh: load };
}

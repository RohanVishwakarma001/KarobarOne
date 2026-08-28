"use client";

import { useCallback, useEffect, useState } from "react";
import {
  ApiError,
  type Wishlist,
  type WishlistItem,
  addWishlistItem,
  createWishlist,
  listWishlists,
  listWishlistItems,
  removeWishlistItem,
} from "@/lib/api/github";
import { useCustomerSession } from "./use-customer-session";

const WISHLIST_ID_KEY = "karobar_wishlist_id";

/** No by-customer filter server-side — cache the wishlistId locally, same pattern as useCart. */
export function useWishlist() {
  const { customerId, ready } = useCustomerSession();
  const [wishlist, setWishlist] = useState<Wishlist | null>(null);
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!ready || !customerId) return;
    setLoading(true);
    setError(null);
    try {
      let active: Wishlist | null = null;
      const cachedId = window.localStorage.getItem(WISHLIST_ID_KEY);
      if (cachedId) {
        const all = await listWishlists();
        active = all.find((w) => w.id === cachedId) ?? null;
      }
      if (!active) {
        active = await createWishlist(customerId);
        window.localStorage.setItem(WISHLIST_ID_KEY, active.id);
      }
      setWishlist(active);
      const allItems = await listWishlistItems();
      setItems(allItems.filter((i) => i.wishlist_id === active!.id));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not load your wishlist.");
    } finally {
      setLoading(false);
    }
  }, [customerId, ready]);

  useEffect(() => {
    load();
  }, [load]);

  const addItem = useCallback(
    async (productId: string, productVariantId?: string) => {
      if (!wishlist) return;
      const item = await addWishlistItem({ wishlist_id: wishlist.id, product_id: productId, product_variant_id: productVariantId });
      setItems((prev) => [...prev, item]);
    },
    [wishlist]
  );

  const removeItem = useCallback(async (wishlistItemId: string) => {
    await removeWishlistItem(wishlistItemId);
    setItems((prev) => prev.filter((i) => i.id !== wishlistItemId));
  }, []);

  return { customerId, wishlist, items, loading, error, addItem, removeItem, refresh: load };
}

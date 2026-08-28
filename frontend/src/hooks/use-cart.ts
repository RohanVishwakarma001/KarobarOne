"use client";

import { useCallback, useEffect, useState } from "react";
import {
  ApiError,
  type Cart,
  type CartItem,
  addCartItem,
  createCart,
  getCart,
  listCartItems,
  removeCartItem,
  updateCartItem,
} from "@/lib/api/github";
import { useCustomerSession } from "./use-customer-session";

const CART_ID_KEY = "karobar_cart_id";

/**
 * There's no `GET /cart?customer_id=` filter on the backend, so we cache the
 * cartId locally right after creation and reuse it — re-verifying it still
 * exists on load, and creating a fresh one if it doesn't (e.g. cleared DB).
 */
export function useCart() {
  const { customerId, ready } = useCustomerSession();
  const [cart, setCart] = useState<Cart | null>(null);
  const [items, setItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!ready || !customerId) return;
    setLoading(true);
    setError(null);
    try {
      let activeCart: Cart | null = null;
      const cachedId = window.localStorage.getItem(CART_ID_KEY);
      if (cachedId) {
        try {
          activeCart = await getCart(cachedId);
        } catch (e) {
          if (!(e instanceof ApiError && e.status === 404)) throw e;
        }
      }
      if (!activeCart) {
        activeCart = await createCart(customerId);
        window.localStorage.setItem(CART_ID_KEY, activeCart.id);
      }
      setCart(activeCart);
      setItems(await listCartItems(activeCart.id));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not load your cart.");
    } finally {
      setLoading(false);
    }
  }, [customerId, ready]);

  useEffect(() => {
    load();
  }, [load]);

  const addItem = useCallback(
    async (input: { product_id: string; product_variant_id?: string; unit_price: number; quantity?: number }) => {
      if (!cart) return;
      const item = await addCartItem({ cart_id: cart.id, ...input });
      setItems((prev) => [...prev, item]);
    },
    [cart]
  );

  const setQuantity = useCallback(async (cartItemId: string, quantity: number) => {
    if (quantity < 1) return;
    const updated = await updateCartItem(cartItemId, { quantity });
    setItems((prev) => prev.map((i) => (i.id === cartItemId ? updated : i)));
  }, []);

  const removeItem = useCallback(async (cartItemId: string) => {
    await removeCartItem(cartItemId);
    setItems((prev) => prev.filter((i) => i.id !== cartItemId));
  }, []);

  const subtotal = items.reduce((sum, i) => sum + i.line_total, 0);

  return { customerId, cart, items, subtotal, loading, error, addItem, setQuantity, removeItem, refresh: load };
}

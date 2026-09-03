"use client";

// Named use-commerce-cart (not use-cart) to avoid colliding with the
// existing src/hooks/use-cart.ts, which powers the pre-existing /cart page
// and CheckoutForm.tsx against the deprecated /api/v1/github/cart router.
// This one is for the ACTIVE /api/v1/cart router — see docs/api-mapping/commerce.md.

import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  addCartItem,
  applyCartCoupon,
  getCart,
  removeCartItem,
  updateCartItemQuantity,
  type Cart,
} from "@/lib/api/commerce";
import { ApiError } from "@/lib/api/api-client";
import { TENANT_ID, STORE_ID } from "@/lib/api/config";

const GUEST_SESSION_KEY = "karobar_commerce_cart_session_id";

/** A stable anonymous cart identity — there's no customer JWT anywhere in this codebase (see docs/api-mapping/auth.md), so guest carts are keyed off this instead. */
function getOrCreateGuestSessionId(): string {
  if (typeof window === "undefined") return "";
  let sessionId = window.localStorage.getItem(GUEST_SESSION_KEY);
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    window.localStorage.setItem(GUEST_SESSION_KEY, sessionId);
  }
  return sessionId;
}

export function useGuestSessionId(): string {
  const [sessionId, setSessionId] = useState("");
  useEffect(() => setSessionId(getOrCreateGuestSessionId()), []);
  return sessionId;
}

export const commerceCartKeys = {
  detail: (sessionId: string) => ["commerce-cart", TENANT_ID, STORE_ID, sessionId] as const,
};

function errorMessage(err: unknown, fallback: string): string {
  return err instanceof ApiError ? err.message : fallback;
}

export function useCommerceCart(sessionId: string) {
  return useQuery({
    queryKey: commerceCartKeys.detail(sessionId),
    queryFn: () => getCart({ tenantId: TENANT_ID, storeId: STORE_ID, sessionId }),
    enabled: Boolean(sessionId && TENANT_ID && STORE_ID),
    staleTime: 10_000,
  });
}

export function useAddCommerceCartItem(sessionId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: { productId: string; productVariantId?: string; quantity: number; unitPrice: number }) =>
      addCartItem(
        { tenantId: TENANT_ID, storeId: STORE_ID, sessionId, unitPrice: input.unitPrice },
        { productId: input.productId, productVariantId: input.productVariantId, quantity: input.quantity },
      ),
    onSuccess: (cart) => {
      queryClient.setQueryData(commerceCartKeys.detail(sessionId), cart);
      toast.success("Added to cart");
    },
    onError: (err) => toast.error(errorMessage(err, "Couldn't add that to your cart.")),
  });
}

/** Optimistic: the quantity/line-total change is visible immediately, rolled back on failure. */
export function useUpdateCommerceCartItemQuantity(sessionId: string) {
  const queryClient = useQueryClient();
  const queryKey = commerceCartKeys.detail(sessionId);

  return useMutation({
    mutationFn: ({ itemId, quantity }: { itemId: string; quantity: number }) => updateCartItemQuantity(itemId, quantity),
    onMutate: async ({ itemId, quantity }) => {
      await queryClient.cancelQueries({ queryKey });
      const previous = queryClient.getQueryData<Cart>(queryKey);
      if (previous) {
        queryClient.setQueryData<Cart>(queryKey, {
          ...previous,
          items: previous.items.map((item) =>
            item.id === itemId ? { ...item, quantity, lineTotal: (Number(item.unitPrice) * quantity).toFixed(2) } : item,
          ),
        });
      }
      return { previous };
    },
    onError: (err, _vars, context) => {
      if (context?.previous) queryClient.setQueryData(queryKey, context.previous);
      toast.error(errorMessage(err, "Couldn't update the quantity."));
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey }),
  });
}

export function useRemoveCommerceCartItem(sessionId: string) {
  const queryClient = useQueryClient();
  const queryKey = commerceCartKeys.detail(sessionId);

  return useMutation({
    mutationFn: (itemId: string) => removeCartItem(itemId),
    onMutate: async (itemId) => {
      await queryClient.cancelQueries({ queryKey });
      const previous = queryClient.getQueryData<Cart>(queryKey);
      if (previous) {
        queryClient.setQueryData<Cart>(queryKey, { ...previous, items: previous.items.filter((i) => i.id !== itemId) });
      }
      return { previous };
    },
    onError: (err, _vars, context) => {
      if (context?.previous) queryClient.setQueryData(queryKey, context.previous);
      toast.error(errorMessage(err, "Couldn't remove that item."));
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey }),
  });
}

export function useApplyCommerceCoupon(sessionId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ cartId, couponCode, customerId }: { cartId: string; couponCode: string; customerId: string }) =>
      applyCartCoupon(cartId, { couponCode, customerId }),
    onSuccess: ({ cart, discountAmount }) => {
      queryClient.setQueryData(commerceCartKeys.detail(sessionId), cart);
      toast.success(`Coupon applied — you saved ₹${discountAmount}`);
    },
    onError: (err) => toast.error(errorMessage(err, "That coupon couldn't be applied.")),
  });
}

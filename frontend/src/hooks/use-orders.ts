"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { createOrder, getOrder, getOrderStatusHistory, type OrderItemInput } from "@/lib/api/commerce";
import { ApiError } from "@/lib/api/api-client";

export const orderKeys = {
  detail: (orderId: string) => ["order", orderId] as const,
  history: (orderId: string) => ["order-history", orderId] as const,
};

function errorMessage(err: unknown, fallback: string): string {
  return err instanceof ApiError ? err.message : fallback;
}

export function useOrder(orderId: string | null) {
  return useQuery({
    queryKey: orderKeys.detail(orderId ?? ""),
    queryFn: () => getOrder(orderId as string),
    enabled: Boolean(orderId),
  });
}

export function useOrderHistory(orderId: string | null) {
  return useQuery({
    queryKey: orderKeys.history(orderId ?? ""),
    queryFn: () => getOrderStatusHistory(orderId as string),
    enabled: Boolean(orderId),
  });
}

export function useCreateOrder() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: {
      tenantId: string;
      storeId: string;
      customerId: string;
      billingAddressId: string;
      shippingAddressId: string;
      items: OrderItemInput[];
      shippingAmount?: number;
      customerNote?: string;
      cartId?: string;
    }) => createOrder(input),
    onSuccess: (order) => {
      queryClient.setQueryData(orderKeys.detail(order.id), order);
    },
    onError: (err) => toast.error(errorMessage(err, "Couldn't place your order.")),
  });
}

"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { deleteProduct, getProduct, updateProduct, type ProductResponse, type ProductUpdateInput } from "@/lib/api/products";
import { ApiError } from "@/lib/api/api-client";

export const productKeys = {
  detail: (productId: string) => ["product", productId] as const,
};

export function useProduct(productId: string) {
  return useQuery({
    queryKey: productKeys.detail(productId),
    queryFn: () => getProduct(productId),
    enabled: Boolean(productId),
  });
}

export function useUpdateProduct(productId: string) {
  const queryClient = useQueryClient();
  const queryKey = productKeys.detail(productId);

  return useMutation({
    mutationFn: (input: ProductUpdateInput) => updateProduct(productId, input),
    onMutate: async (input) => {
      await queryClient.cancelQueries({ queryKey });
      const previous = queryClient.getQueryData<ProductResponse>(queryKey);
      if (previous) {
        queryClient.setQueryData<ProductResponse>(queryKey, { ...previous, ...input });
      }
      return { previous };
    },
    onError: (err, _input, context) => {
      if (context?.previous) queryClient.setQueryData(queryKey, context.previous);
      toast.error(err instanceof ApiError ? err.message : "Couldn't save those changes.");
    },
    onSuccess: () => {
      toast.success("Product updated.");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });
}

/** Optimistically flips the cached product to ARCHIVED (delete_product is a soft delete) before the request settles, rolling back on failure. */
export function useDeleteProduct(productId: string) {
  const queryClient = useQueryClient();
  const queryKey = productKeys.detail(productId);

  return useMutation({
    mutationFn: () => deleteProduct(productId),
    onMutate: async () => {
      await queryClient.cancelQueries({ queryKey });
      const previous = queryClient.getQueryData<ProductResponse>(queryKey);
      if (previous) {
        queryClient.setQueryData<ProductResponse>(queryKey, { ...previous, status: "ARCHIVED", deletedAt: new Date().toISOString() });
      }
      return { previous };
    },
    onError: (err, _vars, context) => {
      if (context?.previous) queryClient.setQueryData(queryKey, context.previous);
      toast.error(err instanceof ApiError ? err.message : "Couldn't delete this product.");
    },
    onSuccess: () => {
      toast.success("Product deleted.");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });
}

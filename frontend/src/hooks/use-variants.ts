"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  createProductVariant,
  deleteProductVariant,
  deleteVariantImage,
  listProductVariants,
  listVariantImages,
  replaceProductVariant,
  uploadVariantImage,
  type VariantCreateForProductInput,
  type VariantResponse,
} from "@/lib/api/variants";
import { ApiError } from "@/lib/api/coreClient";

export const variantKeys = {
  list: (productId: string) => ["product-variants", productId] as const,
  images: (productId: string, variantId: string) => ["variant-images", productId, variantId] as const,
};

export function useVariantImages(productId: string, variantId: string | null) {
  return useQuery({
    queryKey: variantKeys.images(productId, variantId ?? ""),
    queryFn: () => listVariantImages(productId, variantId as string),
    enabled: Boolean(productId && variantId),
  });
}

export function useDeleteVariantImage(productId: string, variantId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (imageId: string) => deleteVariantImage(imageId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: variantKeys.images(productId, variantId) });
    },
    onError: (err) => {
      toast.error(errorMessage(err, "Couldn't remove that image."));
    },
  });
}

function errorMessage(err: unknown, fallback: string): string {
  if (err instanceof ApiError) return err.message;
  if (err instanceof Error) return err.message;
  return fallback;
}

export function useProductVariants(productId: string) {
  return useQuery({
    queryKey: variantKeys.list(productId),
    queryFn: () => listProductVariants(productId),
    enabled: Boolean(productId),
  });
}

export function useCreateVariant(productId: string, tenantId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: VariantCreateForProductInput) => createProductVariant(productId, tenantId, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: variantKeys.list(productId) });
    },
    onError: (err) => {
      toast.error(errorMessage(err, "Couldn't create that variant."));
    },
  });
}

export function useUpdateVariant(productId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ variantId, input }: { variantId: string; input: VariantCreateForProductInput }) =>
      replaceProductVariant(productId, variantId, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: variantKeys.list(productId) });
    },
    onError: (err) => {
      toast.error(errorMessage(err, "Couldn't save that variant."));
    },
  });
}

export function useDeleteVariant(productId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (variantId: string) => deleteProductVariant(productId, variantId),
    onMutate: async (variantId: string) => {
      await queryClient.cancelQueries({ queryKey: variantKeys.list(productId) });
      const previous = queryClient.getQueryData<VariantResponse[]>(variantKeys.list(productId));
      if (previous) {
        queryClient.setQueryData<VariantResponse[]>(
          variantKeys.list(productId),
          previous.filter((v) => v.id !== variantId),
        );
      }
      return { previous };
    },
    onError: (err, _variantId, context) => {
      if (context?.previous) queryClient.setQueryData(variantKeys.list(productId), context.previous);
      toast.error(errorMessage(err, "Couldn't delete that variant."));
    },
    onSuccess: () => {
      toast.success("Variant deleted.");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: variantKeys.list(productId) });
    },
  });
}

export function useUploadVariantImage() {
  return useMutation({
    mutationFn: uploadVariantImage,
    onError: (err) => {
      toast.error(errorMessage(err, "Image upload failed."));
    },
  });
}

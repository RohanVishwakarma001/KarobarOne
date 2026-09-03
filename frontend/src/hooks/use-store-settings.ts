"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  getStoreSettings,
  updateStoreSettings,
  type WebsiteSettingResponse,
  type WebsiteSettingUpdateInput,
} from "@/lib/api/website-settings";
import { ApiError } from "@/lib/api/api-client";

export const storeSettingsKeys = {
  detail: (storeId: string) => ["store-settings", storeId] as const,
};

export function useStoreSettings(storeId: string) {
  return useQuery({
    queryKey: storeSettingsKeys.detail(storeId),
    queryFn: () => getStoreSettings(storeId),
    enabled: Boolean(storeId),
  });
}

/**
 * Optimistic update: the toggle/input reflects the new value immediately
 * (onMutate), rolls back to the exact previous snapshot on failure (onError),
 * and reconciles with the server's copy either way (onSettled) — the
 * standard TanStack optimistic-update triad.
 */
export function useUpdateStoreSettings(storeId: string) {
  const queryClient = useQueryClient();
  const queryKey = storeSettingsKeys.detail(storeId);

  return useMutation({
    mutationFn: (input: WebsiteSettingUpdateInput) => updateStoreSettings(storeId, input),
    onMutate: async (input) => {
      await queryClient.cancelQueries({ queryKey });
      const previous = queryClient.getQueryData<WebsiteSettingResponse>(queryKey);
      if (previous) {
        queryClient.setQueryData<WebsiteSettingResponse>(queryKey, { ...previous, ...input });
      }
      return { previous };
    },
    onError: (err, _input, context) => {
      if (context?.previous) queryClient.setQueryData(queryKey, context.previous);
      toast.error(err instanceof ApiError ? err.message : "Couldn't save those settings.");
    },
    onSuccess: () => {
      toast.success("Settings saved.");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });
}

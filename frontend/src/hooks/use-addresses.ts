"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  createAddress,
  deleteAddress,
  listCustomerAddresses,
  updateAddress,
  type AddressCreateInput,
  type AddressUpdateInput,
} from "@/lib/api/addresses";
import { listCustomerSessions } from "@/lib/api/customerSessions";
import { ApiError } from "@/lib/api/api-client";

export const addressKeys = {
  list: (customerId: string) => ["customer-addresses", customerId] as const,
};

export const sessionKeys = {
  list: (customerId: string) => ["customer-sessions", customerId] as const,
};

function errorMessage(err: unknown, fallback: string): string {
  return err instanceof ApiError ? err.message : fallback;
}

export function useCustomerAddresses(customerId: string | null) {
  return useQuery({
    queryKey: addressKeys.list(customerId ?? ""),
    queryFn: () => listCustomerAddresses(customerId as string),
    enabled: Boolean(customerId),
  });
}

export function useCustomerSessions(customerId: string | null) {
  return useQuery({
    queryKey: sessionKeys.list(customerId ?? ""),
    queryFn: () => listCustomerSessions(customerId as string),
    enabled: Boolean(customerId),
  });
}

export function useCreateAddress(customerId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: Omit<AddressCreateInput, "customerId">) => createAddress({ customerId, ...input }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: addressKeys.list(customerId) });
      toast.success("Address added.");
    },
    onError: (err) => toast.error(errorMessage(err, "Couldn't add that address.")),
  });
}

export function useUpdateAddress(customerId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ addressId, input }: { addressId: string; input: AddressUpdateInput }) => updateAddress(addressId, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: addressKeys.list(customerId) });
      toast.success("Address updated.");
    },
    onError: (err) => toast.error(errorMessage(err, "Couldn't update that address.")),
  });
}

export function useDeleteAddress(customerId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (addressId: string) => deleteAddress(addressId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: addressKeys.list(customerId) });
      toast.success("Address removed.");
    },
    onError: (err) => toast.error(errorMessage(err, "Couldn't remove that address.")),
  });
}

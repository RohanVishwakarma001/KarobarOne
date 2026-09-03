"use client";

import { useMutation, useQuery, useQueryClient, keepPreviousData } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  createCustomer,
  deleteCustomer,
  getCustomer,
  listCustomers,
  listTrashedCustomers,
  restoreCustomer,
  updateCustomer,
  type CustomerCreateInput,
  type CustomerListFilters,
  type CustomerResponse,
  type CustomerUpdateInput,
  type PaginatedCustomers,
} from "@/lib/api/customers";
import { ApiError } from "@/lib/api/coreClient";

export const customerKeys = {
  all: (tenantId: string) => ["customers", tenantId] as const,
  lists: (tenantId: string) => [...customerKeys.all(tenantId), "list"] as const,
  list: (tenantId: string, filters: CustomerListFilters) => [...customerKeys.lists(tenantId), filters] as const,
  details: (tenantId: string) => [...customerKeys.all(tenantId), "detail"] as const,
  detail: (tenantId: string, customerId: string) => [...customerKeys.details(tenantId), customerId] as const,
  trash: (tenantId: string, page: number, pageSize: number) =>
    [...customerKeys.all(tenantId), "trash", page, pageSize] as const,
};

function errorMessage(err: unknown, fallback: string): string {
  return err instanceof ApiError ? err.message : fallback;
}

export function useCustomers(tenantId: string, filters: CustomerListFilters) {
  return useQuery({
    queryKey: customerKeys.list(tenantId, filters),
    queryFn: () => listCustomers(tenantId, filters),
    enabled: Boolean(tenantId),
    placeholderData: keepPreviousData,
  });
}

export function useCustomer(tenantId: string, customerId: string | null) {
  return useQuery({
    queryKey: customerKeys.detail(tenantId, customerId ?? ""),
    queryFn: () => getCustomer(tenantId, customerId as string),
    enabled: Boolean(tenantId && customerId),
  });
}

export function useTrashedCustomers(tenantId: string, page: number, pageSize: number) {
  return useQuery({
    queryKey: customerKeys.trash(tenantId, page, pageSize),
    queryFn: () => listTrashedCustomers(tenantId, { page, pageSize }),
    enabled: Boolean(tenantId),
    placeholderData: keepPreviousData,
  });
}

export function useCreateCustomer(tenantId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: CustomerCreateInput) => createCustomer(input),
    onSuccess: (created) => {
      queryClient.invalidateQueries({ queryKey: customerKeys.lists(tenantId) });
      toast.success(`${created.firstName} ${created.lastName ?? ""}`.trim() + " added.");
    },
    onError: (err) => {
      toast.error(errorMessage(err, "Couldn't create the customer."));
    },
  });
}

type UpdateVars = { customerId: string; input: CustomerUpdateInput };

export function useUpdateCustomer(tenantId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ customerId, input }: UpdateVars) => updateCustomer(tenantId, customerId, input),
    onMutate: async ({ customerId, input }) => {
      const detailKey = customerKeys.detail(tenantId, customerId);
      await queryClient.cancelQueries({ queryKey: detailKey });
      const previousDetail = queryClient.getQueryData<CustomerResponse>(detailKey);

      if (previousDetail) {
        queryClient.setQueryData<CustomerResponse>(detailKey, { ...previousDetail, ...input });
      }

      // Also patch any cached list pages so the table reflects the edit immediately.
      const previousLists = queryClient.getQueriesData<PaginatedCustomers>({ queryKey: customerKeys.lists(tenantId) });
      for (const [key, page] of previousLists) {
        if (!page) continue;
        queryClient.setQueryData<PaginatedCustomers>(key, {
          ...page,
          data: page.data.map((c) => (c.id === customerId ? { ...c, ...input } : c)),
        });
      }

      return { previousDetail, previousLists };
    },
    onError: (err, { customerId }, context) => {
      if (context?.previousDetail) {
        queryClient.setQueryData(customerKeys.detail(tenantId, customerId), context.previousDetail);
      }
      context?.previousLists?.forEach(([key, page]) => {
        queryClient.setQueryData(key, page);
      });
      toast.error(errorMessage(err, "Couldn't save those changes."));
    },
    onSuccess: () => {
      toast.success("Customer updated.");
    },
    onSettled: (_data, _err, { customerId }) => {
      queryClient.invalidateQueries({ queryKey: customerKeys.detail(tenantId, customerId) });
      queryClient.invalidateQueries({ queryKey: customerKeys.lists(tenantId) });
    },
  });
}

export function useDeleteCustomer(tenantId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (customerId: string) => deleteCustomer(tenantId, customerId),
    onMutate: async (customerId: string) => {
      await queryClient.cancelQueries({ queryKey: customerKeys.lists(tenantId) });
      const previousLists = queryClient.getQueriesData<PaginatedCustomers>({ queryKey: customerKeys.lists(tenantId) });
      for (const [key, page] of previousLists) {
        if (!page) continue;
        queryClient.setQueryData<PaginatedCustomers>(key, {
          ...page,
          total: Math.max(0, page.total - (page.data.some((c) => c.id === customerId) ? 1 : 0)),
          data: page.data.filter((c) => c.id !== customerId),
        });
      }
      return { previousLists };
    },
    onError: (err, _customerId, context) => {
      context?.previousLists?.forEach(([key, page]) => {
        queryClient.setQueryData(key, page);
      });
      toast.error(errorMessage(err, "Couldn't delete that customer."));
    },
    onSuccess: () => {
      toast.success("Customer moved to trash.");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: customerKeys.all(tenantId) });
    },
  });
}

export function useRestoreCustomer(tenantId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (customerId: string) => restoreCustomer(tenantId, customerId),
    onSuccess: (restored) => {
      toast.success(`${restored.firstName} restored.`);
      queryClient.invalidateQueries({ queryKey: customerKeys.all(tenantId) });
    },
    onError: (err) => {
      toast.error(errorMessage(err, "Couldn't restore that customer."));
    },
  });
}

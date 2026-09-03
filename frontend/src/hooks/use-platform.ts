"use client";

import { useMutation, useQuery, useQueryClient, keepPreviousData } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  analyzeKeywordDensity,
  assignTenantPlan,
  auditSeo,
  calculateSeoScore,
  downgradeTenantPlan,
  generateAiSeoSuggestions,
  generateWebsiteAIContent,
  getFullHealth,
  getTenantPlan,
  grantStoreStaffPermission,
  listAuditLogs,
  listPermissions,
  listPlans,
  listRoles,
  listStoreStaffPermissions,
  listTenants,
  listWebsitePublishLogs,
  revokeStoreStaffPermission,
  upgradeTenantPlan,
  type AiSeoSuggestionRequest,
  type AuditLogFilters,
  type KeywordDensityRequest,
  type SeoAuditRequest,
  type SeoScoreRequest,
  type StoreStaffPermissionGrant,
  type TenantListFilters,
  type WebsiteAIGenerateRequest,
} from "@/lib/api/platform";
import { ApiError } from "@/lib/api/coreClient";

function errorMessage(err: unknown, fallback: string): string {
  return err instanceof ApiError ? err.message : fallback;
}

// ============================================================================
// Query keys
// ============================================================================

export const platformKeys = {
  plans: () => ["platform", "plans"] as const,
  tenants: (filters: TenantListFilters) => ["platform", "tenants", filters] as const,
  tenantPlan: (tenantId: string) => ["platform", "tenant-plan", tenantId] as const,
  roles: () => ["platform", "roles"] as const,
  permissions: () => ["platform", "permissions"] as const,
  storeStaffPermissions: (userId: string, storeId: string) =>
    ["platform", "store-staff-permissions", userId, storeId] as const,
  fullHealth: () => ["platform", "health", "full"] as const,
  auditLogs: (filters: AuditLogFilters) => ["platform", "audit-logs", filters] as const,
  publishLogs: (storeId: string) => ["platform", "publish-logs", storeId] as const,
};

// ============================================================================
// Tenant & Plan Switcher Dashboard
// ============================================================================

export function usePlatformPlans() {
  return useQuery({
    queryKey: platformKeys.plans(),
    queryFn: () => listPlans(),
  });
}

export function usePlatformTenants(filters: TenantListFilters) {
  return useQuery({
    queryKey: platformKeys.tenants(filters),
    queryFn: () => listTenants(filters),
    placeholderData: keepPreviousData,
  });
}

export function useTenantPlan(tenantId: string | null) {
  return useQuery({
    queryKey: platformKeys.tenantPlan(tenantId ?? ""),
    queryFn: () => getTenantPlan(tenantId as string),
    enabled: Boolean(tenantId),
  });
}

type PlanChangeVars = { tenantId: string; planId: string; hasExistingPlan: boolean; direction: "upgrade" | "downgrade" };

/** Assigns a first plan, or calls upgrade/downgrade for a tenant that already has one — same UI action either way. */
export function useChangeTenantPlan() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ tenantId, planId, hasExistingPlan, direction }: PlanChangeVars) => {
      const planStartDate = new Date().toISOString().slice(0, 10);
      if (!hasExistingPlan) {
        return assignTenantPlan(tenantId, { planId, planStartDate });
      }
      return direction === "upgrade"
        ? upgradeTenantPlan(tenantId, { planId, planStartDate })
        : downgradeTenantPlan(tenantId, { planId, planStartDate });
    },
    onSuccess: (_result, { tenantId, direction }) => {
      queryClient.invalidateQueries({ queryKey: platformKeys.tenantPlan(tenantId) });
      toast.success(direction === "upgrade" ? "Plan upgraded." : "Plan changed.");
    },
    onError: (err) => {
      toast.error(errorMessage(err, "Couldn't change the plan."));
    },
  });
}

// ============================================================================
// Staff & Permissions Matrix
// ============================================================================

export function usePlatformRoles() {
  return useQuery({
    queryKey: platformKeys.roles(),
    queryFn: () => listRoles(),
  });
}

export function usePlatformPermissions() {
  return useQuery({
    queryKey: platformKeys.permissions(),
    queryFn: () => listPermissions(),
  });
}

export function useStoreStaffPermissions(userId: string | null, storeId: string | null) {
  return useQuery({
    queryKey: platformKeys.storeStaffPermissions(userId ?? "", storeId ?? ""),
    queryFn: () => listStoreStaffPermissions(userId as string, storeId as string),
    enabled: Boolean(userId && storeId),
  });
}

type ToggleGrantVars = {
  userId: string;
  storeId: string;
  permissionId: string;
  /** The existing grant record to revoke, if the checkbox is being unchecked. */
  existingGrant: StoreStaffPermissionGrant | undefined;
};

/** Optimistically flips one cell in the permission matrix — grants if unchecked, revokes if checked. */
export function useTogglePermissionGrant() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ userId, storeId, permissionId, existingGrant }: ToggleGrantVars) => {
      if (existingGrant) {
        await revokeStoreStaffPermission(userId, existingGrant.id);
        return null;
      }
      return grantStoreStaffPermission(userId, { storeId, permissionId });
    },
    onMutate: async ({ userId, storeId, permissionId, existingGrant }) => {
      const key = platformKeys.storeStaffPermissions(userId, storeId);
      await queryClient.cancelQueries({ queryKey: key });
      const previous = queryClient.getQueryData<StoreStaffPermissionGrant[]>(key);

      queryClient.setQueryData<StoreStaffPermissionGrant[]>(key, (current = []) =>
        existingGrant
          ? current.filter((g) => g.id !== existingGrant.id)
          : [
              ...current,
              {
                id: `optimistic-${permissionId}`,
                userId,
                storeId,
                permissionId,
                grantedBy: null,
                createdAt: new Date().toISOString(),
              },
            ],
      );
      return { previous, key };
    },
    onError: (err, _vars, context) => {
      if (context) queryClient.setQueryData(context.key, context.previous);
      toast.error(errorMessage(err, "Couldn't update that permission."));
    },
    onSettled: (_data, _err, { userId, storeId }) => {
      queryClient.invalidateQueries({ queryKey: platformKeys.storeStaffPermissions(userId, storeId) });
    },
  });
}

// ============================================================================
// SEO & AI Assistant Panel
// ============================================================================

export function useSeoScore() {
  return useMutation({
    mutationFn: (input: SeoScoreRequest) => calculateSeoScore(input),
    onError: (err) => toast.error(errorMessage(err, "Couldn't calculate the SEO score.")),
  });
}

export function useSeoAudit() {
  return useMutation({
    mutationFn: (input: SeoAuditRequest) => auditSeo(input),
    onError: (err) => toast.error(errorMessage(err, "Couldn't run the SEO audit.")),
  });
}

export function useAiSeoSuggestions() {
  return useMutation({
    mutationFn: (input: AiSeoSuggestionRequest) => generateAiSeoSuggestions(input),
    onError: (err) => toast.error(errorMessage(err, "Couldn't generate AI suggestions.")),
  });
}

export function useKeywordDensity() {
  return useMutation({
    mutationFn: (input: KeywordDensityRequest) => analyzeKeywordDensity(input),
    onError: (err) => toast.error(errorMessage(err, "Couldn't analyze keyword density.")),
  });
}

export function useGenerateAIContent() {
  return useMutation({
    mutationFn: (input: WebsiteAIGenerateRequest) => generateWebsiteAIContent(input),
    onSuccess: () => toast.success("Draft generated."),
    onError: (err) => toast.error(errorMessage(err, "Couldn't generate content.")),
  });
}

// ============================================================================
// System Health & Audit Viewer
// ============================================================================

export function useFullHealth() {
  return useQuery({
    queryKey: platformKeys.fullHealth(),
    queryFn: () => getFullHealth(),
    // Polled, not one-shot — this backs the dashboard's live uptime badges.
    refetchInterval: 30_000,
  });
}

export function useAuditLogs(filters: AuditLogFilters) {
  return useQuery({
    queryKey: platformKeys.auditLogs(filters),
    queryFn: () => listAuditLogs(filters),
    placeholderData: keepPreviousData,
  });
}

export function useWebsitePublishLogs(storeId: string | null) {
  return useQuery({
    queryKey: platformKeys.publishLogs(storeId ?? ""),
    queryFn: () => listWebsitePublishLogs(storeId as string),
    enabled: Boolean(storeId),
  });
}

import { ApiError, coreDelete, coreGet, corePost } from "./coreClient";

// ============================================================================
// Shared envelope — mirrors app.schemas.common.PaginatedResponse[T] exactly
// (items/total/skip/limit, NOT the page/pageSize/data shape customers.ts uses —
// tenants/plans/etc. share this one generic wrapper across the whole module).
// ============================================================================

export type PaginatedItems<T> = {
  items: T[];
  total: number;
  skip: number;
  limit: number;
};

// ============================================================================
// Plans & Plan Features — mirrors app.schemas.subscriptionPlan / planFeature
// ============================================================================

export type PlanFeature = {
  id: string;
  planId: string;
  featureName: string;
  featureCode: string;
  featureValue: unknown;
  createdAt: string;
};

export type Plan = {
  id: string;
  planCode: string;
  planName: string;
  monthlyPrice: string;
  transactionCommissionPercent: string;
  isActive: boolean;
  features: PlanFeature[];
  createdAt: string;
};

export function listPlans(activeOnly = false): Promise<PaginatedItems<Plan>> {
  return coreGet<PaginatedItems<Plan>>(`/plans?skip=0&limit=100&activeOnly=${activeOnly}`);
}

// ============================================================================
// Tenants — mirrors app.schemas.tenant
// ============================================================================

export type TenantCompact = {
  id: string;
  businessName: string;
  legalName: string;
  email: string;
  mobile: string;
  city: string;
  state: string;
  businessType: string;
  statusId: number | null;
  isActive: boolean;
  createdAt: string;
};

export type TenantListFilters = {
  skip?: number;
  limit?: number;
  city?: string;
  state?: string;
  businessType?: string;
};

export function listTenants(filters: TenantListFilters = {}): Promise<PaginatedItems<TenantCompact>> {
  const params = new URLSearchParams();
  params.set("skip", String(filters.skip ?? 0));
  params.set("limit", String(filters.limit ?? 100));
  if (filters.city) params.set("city", filters.city);
  if (filters.state) params.set("state", filters.state);
  if (filters.businessType) params.set("businessType", filters.businessType);
  return coreGet<PaginatedItems<TenantCompact>>(`/tenants?${params.toString()}`);
}

// ============================================================================
// Tenant <-> Plan mapping — mirrors app.schemas.tenantPlan
// ============================================================================

export type TenantPlanMapping = {
  id: string;
  tenantId: string;
  planId: string;
  planStartDate: string;
  planEndDate: string | null;
  planUpdateAt: string | null;
  autoRenew: boolean;
  planChange: boolean;
  changeReason: string | null;
  statusId: number | null;
  plan: {
    id: string;
    planCode: string;
    planName: string;
    monthlyPrice: string;
    transactionCommissionPercent: string;
    isActive: boolean;
    createdAt: string;
  } | null;
};

/** Returns null (instead of throwing) when the tenant has no plan mapping yet — a 404 from the backend. */
export async function getTenantPlan(tenantId: string): Promise<TenantPlanMapping | null> {
  try {
    return await coreGet<TenantPlanMapping>(`/tenants/${tenantId}/plan`);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  }
}

export function assignTenantPlan(
  tenantId: string,
  input: { planId: string; planStartDate: string; planEndDate?: string | null; autoRenew?: boolean },
): Promise<TenantPlanMapping> {
  return corePost<TenantPlanMapping>(`/tenants/${tenantId}/plan`, input);
}

export function upgradeTenantPlan(
  tenantId: string,
  input: { planId: string; planStartDate: string },
): Promise<TenantPlanMapping> {
  return corePost<TenantPlanMapping>(`/tenants/${tenantId}/upgrade`, input);
}

export function downgradeTenantPlan(
  tenantId: string,
  input: { planId: string; planStartDate: string },
): Promise<TenantPlanMapping> {
  return corePost<TenantPlanMapping>(`/tenants/${tenantId}/downgrade`, input);
}

// ============================================================================
// Roles — mirrors app.schemas.role
// ============================================================================

export type Role = {
  id: string;
  roleName: string;
  roleCode: string;
  description: string | null;
  isSystemRole: boolean;
  createdAt: string;
  updatedAt: string;
};

export function listRoles(): Promise<Role[]> {
  return coreGet<Role[]>("/roles/");
}

// ============================================================================
// Permissions — mirrors app.schemas.permission
// ============================================================================

export type Permission = {
  id: string;
  permissionName: string;
  permissionCode: string;
  description: string | null;
  createdAt: string;
};

export function listPermissions(): Promise<Permission[]> {
  return coreGet<Permission[]>("/permissions/");
}

// ============================================================================
// Store-staff permission overrides — mirrors app.schemas.storeStaffPermission
// (POST /users/{userId}/store-permissions/, GET requires a storeId filter,
// DELETE /users/{userId}/store-permissions/{recordId})
// ============================================================================

export type StoreStaffPermissionGrant = {
  id: string;
  userId: string;
  storeId: string;
  permissionId: string;
  grantedBy: string | null;
  createdAt: string;
};

export function listStoreStaffPermissions(userId: string, storeId: string): Promise<StoreStaffPermissionGrant[]> {
  return coreGet<StoreStaffPermissionGrant[]>(`/users/${userId}/store-permissions/?storeId=${storeId}`);
}

export function grantStoreStaffPermission(
  userId: string,
  input: { storeId: string; permissionId: string; grantedBy?: string | null },
): Promise<StoreStaffPermissionGrant> {
  return corePost<StoreStaffPermissionGrant>(`/users/${userId}/store-permissions/`, input);
}

export function revokeStoreStaffPermission(userId: string, recordId: string): Promise<void> {
  return coreDelete<void>(`/users/${userId}/store-permissions/${recordId}`);
}

// ============================================================================
// SEO Metadata + AI scoring — mirrors app.schemas.seoMetadata
// ============================================================================

export type SeoScoreRequest = {
  metaTitle?: string | null;
  metaDescription?: string | null;
  canonicalUrl?: string | null;
  slug?: string | null;
  content?: string | null;
  robotsIndex?: boolean;
  robotsFollow?: boolean;
};

export type SeoScoreResult = {
  seoScore: number;
  grade: string;
  suggestions: string[];
};

export function calculateSeoScore(input: SeoScoreRequest): Promise<SeoScoreResult> {
  return corePost<SeoScoreResult>("/seo-metadata/score", input);
}

export type SeoAuditRequest = SeoScoreRequest;

export type SeoAuditResult = {
  seoScore: number;
  grade: string;
  titleLength: number;
  descriptionLength: number;
  contentLength: number;
  wordCount: number;
  keywordDensity: number;
  readability: string;
  canonical: boolean;
  robots: boolean;
  issues: string[];
  recommendations: string[];
};

export function auditSeo(input: SeoAuditRequest): Promise<SeoAuditResult> {
  return corePost<SeoAuditResult>("/seo-metadata/audit", input);
}

export type AiSeoSuggestionRequest = {
  metaTitle?: string | null;
  metaDescription?: string | null;
  content?: string | null;
};

export type AiSeoSuggestionResult = {
  improvedTitle: string;
  improvedDescription: string;
  keywords: string[];
};

export function generateAiSeoSuggestions(input: AiSeoSuggestionRequest): Promise<AiSeoSuggestionResult> {
  return corePost<AiSeoSuggestionResult>("/seo-metadata/ai-suggestions", input);
}

export type KeywordDensityRequest = { content: string; targetKeyword: string };

export type KeywordDensityResult = {
  keyword: string;
  count: number;
  totalWords: number;
  density: number;
  status: string;
  recommendation: string;
};

export function analyzeKeywordDensity(input: KeywordDensityRequest): Promise<KeywordDensityResult> {
  return corePost<KeywordDensityResult>("/seo-metadata/keyword-density", input);
}

// ============================================================================
// AI Copy Generator — mirrors app.schemas.websiteAIGeneration / websiteAIContent
// ============================================================================

export type WebsiteAIGenerateRequest = {
  storeId: string;
  contentType: string;
  instructions?: string | null;
};

export type WebsiteAIContent = {
  id: string;
  storeId: string;
  contentType: string;
  content: string | null;
  metadata: unknown;
  status: string;
  createdAt: string;
  updatedAt: string;
};

export function generateWebsiteAIContent(input: WebsiteAIGenerateRequest): Promise<WebsiteAIContent> {
  return corePost<WebsiteAIContent>("/website-ai/generate", input);
}

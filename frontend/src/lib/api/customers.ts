import { coreDelete, coreGet, corePatch, corePost, withTenant } from "./coreClient";

/**
 * Mirrors app/schemas/customers.py CustomerBase's status field_validator
 * exactly (backend/app/api/v1/endpoints/customers.py + customers.py schema) —
 * this is the exhaustive set, not an open string, so every switch/map over
 * it is checked by the compiler when a status is ever added or removed here.
 */
export const CUSTOMER_STATUSES = ["ACTIVE", "INACTIVE", "BLOCKED"] as const;
export type CustomerStatus = (typeof CUSTOMER_STATUSES)[number];

/** Mirrors app.schemas.common.APIResponse[T] exactly. */
export type APIResponse<T> = {
  success: boolean;
  data: T;
  message: string;
};

/** Mirrors app.schemas.customers.CustomerResponse. */
export type CustomerResponse = {
  id: string;
  tenantId: string;
  storeId: string;
  customerCode: string;
  firstName: string;
  lastName: string | null;
  email: string;
  mobile: string;
  status: CustomerStatus;
  isGuestCustomer: boolean;
  isEmailVerified: boolean;
  isMobileVerified: boolean;
  lastLoginAt: string | null;
  registeredAt: string | null;
  createdAt: string | null;
  updatedAt: string | null;
  deletedAt: string | null;
};

/** Mirrors app.schemas.customers.PaginatedResponse. */
export type PaginatedCustomers = {
  total: number;
  page: number;
  pageSize: number;
  data: CustomerResponse[];
};

/** Mirrors app.schemas.customers.CustomerCreate (minus the server-defaulted customerCode). */
export type CustomerCreateInput = {
  tenantId: string;
  storeId: string;
  firstName: string;
  lastName?: string;
  email: string;
  mobile: string;
  status: CustomerStatus;
  isGuestCustomer: boolean;
  password?: string;
};

/** Mirrors app.schemas.customers.CustomerUpdate — every field optional, PATCH-style. */
export type CustomerUpdateInput = Partial<{
  firstName: string;
  lastName: string;
  email: string;
  mobile: string;
  status: CustomerStatus;
  isEmailVerified: boolean;
  isMobileVerified: boolean;
  isGuestCustomer: boolean;
}>;

export type CustomerListFilters = {
  page?: number;
  pageSize?: number;
  storeId?: string;
  status?: CustomerStatus;
  isGuestCustomer?: boolean;
};

function buildQuery(params: Record<string, string | number | boolean | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined) search.set(key, String(value));
  }
  const qs = search.toString();
  return qs ? `?${qs}` : "";
}

/**
 * GET /api/v1/customers — admin list, staff bearer + tenant scoped (see
 * app/api/v1/endpoints/customers.py::listCustomers). storeId is an
 * additional filter within the tenant, not a substitute for it.
 */
export function listCustomers(tenantId: string, filters: CustomerListFilters = {}): Promise<PaginatedCustomers> {
  const qs = buildQuery({
    page: filters.page ?? 1,
    pageSize: filters.pageSize ?? 20,
    storeId: filters.storeId,
    status: filters.status,
    isGuestCustomer: filters.isGuestCustomer,
  });
  return coreGet<APIResponse<PaginatedCustomers>>(`/customers/${qs}`, withTenant(tenantId)).then((r) => r.data);
}

export function getCustomer(tenantId: string, customerId: string): Promise<CustomerResponse> {
  return coreGet<APIResponse<CustomerResponse>>(`/customers/${customerId}`, withTenant(tenantId)).then((r) => r.data);
}

/** Public storefront registration (no bearer required) — see createCustomer in customers.py. */
export function createCustomer(input: CustomerCreateInput): Promise<CustomerResponse> {
  return corePost<APIResponse<CustomerResponse>>("/customers/", input).then((r) => r.data);
}

export function updateCustomer(
  tenantId: string,
  customerId: string,
  input: CustomerUpdateInput,
): Promise<CustomerResponse> {
  return corePatch<APIResponse<CustomerResponse>>(`/customers/${customerId}`, input, withTenant(tenantId)).then(
    (r) => r.data,
  );
}

/** 204 No Content on success — see deleteCustomer in customers.py. */
export function deleteCustomer(tenantId: string, customerId: string): Promise<void> {
  return coreDelete<void>(`/customers/${customerId}`, withTenant(tenantId));
}

export function restoreCustomer(tenantId: string, customerId: string): Promise<CustomerResponse> {
  return corePost<APIResponse<CustomerResponse>>(`/customers/${customerId}/restore`, undefined, true, withTenant(tenantId)).then(
    (r) => r.data,
  );
}

export function listTrashedCustomers(
  tenantId: string,
  filters: { page?: number; pageSize?: number } = {},
): Promise<PaginatedCustomers> {
  const qs = buildQuery({ page: filters.page ?? 1, pageSize: filters.pageSize ?? 20 });
  return coreGet<APIResponse<PaginatedCustomers>>(`/customers/trash/list${qs}`, withTenant(tenantId)).then(
    (r) => r.data,
  );
}

import { apiGet } from "./api-client";

/** Mirrors app.schemas.customers.CustomerSessionResponse (app/api/v1/endpoints/customerSessions.py — ACTIVE, prefix "/sessions"). */
export type CustomerSession = {
  id: string;
  customerId: string;
  ipAddress: string | null;
  userAgent: string | null;
  loginAt: string;
  logoutAt: string | null;
  expiresAt: string;
  isActive: boolean;
};

export const listCustomerSessions = (customerId: string, activeOnly = false) =>
  apiGet<CustomerSession[]>(`/sessions/customer/${customerId}?active_only=${activeOnly}`, { auth: false, tenant: false });

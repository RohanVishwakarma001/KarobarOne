import { apiGet } from "./api-client";

/** Mirrors app.schemas.approvals's StatusHistoryResponse (app/api/v1/endpoints/statusHistory.py — generic, prefix "/status-history", no APIResponse envelope). */
export type StatusHistoryEvent = {
  id: string;
  tenantId: string;
  entityType: string;
  entityId: string;
  oldStatus: string | null;
  newStatus: string;
  changeReason: string | null;
  changedBy: string;
  changedAt: string | null;
};

export const listStatusHistory = (entityType: string, entityId: string) =>
  apiGet<StatusHistoryEvent[]>(`/status-history/?entityType=${entityType}&entityId=${entityId}`, {
    auth: false,
    tenant: false,
  });

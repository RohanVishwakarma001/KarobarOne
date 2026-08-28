import { apiGet, apiPost, apiPut, apiDelete } from "../client";
import { TENANT_ID, assertStoreConfig } from "../config";

export type NotificationType = "OFFER" | "ORDER" | "BOOKING" | "PAYMENT" | "SYSTEM";
export type NotificationChannel = "EMAIL" | "SMS" | "WHATSAPP" | "IN_APP";
export type NotificationStatus = "PENDING" | "QUEUED" | "SENT" | "FAILED" | "CANCELLED";

export interface Notification {
  id: string;
  tenant_id: string;
  store_id?: string | null;
  customer_id?: string | null;
  entity_type?: string | null;
  entity_id?: string | null;
  notification_type: NotificationType;
  channel: NotificationChannel;
  subject?: string | null;
  message: string;
  status: NotificationStatus;
  scheduled_at?: string | null;
  sent_at?: string | null;
  created_at?: string;
}

/** Persists a notification record only — does not send anything itself. */
export function queueNotification(input: {
  notification_type: NotificationType;
  channel: NotificationChannel;
  message: string;
  store_id?: string;
  customer_id?: string;
  entity_type?: string;
  entity_id?: string;
  subject?: string;
  scheduled_at?: string;
}) {
  assertStoreConfig();
  return apiPost<Notification>("/notifications/", { tenant_id: TENANT_ID, ...input });
}
// No by-customer filter server-side — fetch all and filter client-side.
export const listNotifications = () => apiGet<Notification[]>("/notifications/");
export const getNotification = (notificationId: string) => apiGet<Notification>(`/notifications/${notificationId}`);
export const updateNotification = (
  notificationId: string,
  data: Partial<Pick<Notification, "subject" | "message" | "scheduled_at" | "sent_at" | "status">>
) => apiPut<Notification>(`/notifications/${notificationId}`, data);
export const deleteNotification = (notificationId: string) => apiDelete<void>(`/notifications/${notificationId}`);

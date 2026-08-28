import { coreGet, corePost } from "./coreClient";

export type StoreCreate = {
  tenantId: string;
  storeName: string;
  storeSlug: string;
  tagline?: string;
  email?: string;
  mobile?: string;
  whatsappMobile?: string;
  description?: string;
};

export type StoreResponse = {
  id: string;
  tenantId: string;
  storeName: string;
  storeSlug: string;
  tagline: string | null;
  email: string | null;
  mobile: string | null;
  whatsappMobile: string | null;
  description: string | null;
  isActive: boolean;
  approvalStatus: string;
  createdAt: string;
  updatedAt: string;
};

export const createStore = (data: StoreCreate) => corePost<StoreResponse>("/stores/", data);
export const getStore = (storeId: string) => coreGet<StoreResponse>(`/stores/${storeId}`);
export const listStores = (tenantId?: string) =>
  coreGet<StoreResponse[]>(`/stores/${tenantId ? `?tenantId=${tenantId}` : ""}`);

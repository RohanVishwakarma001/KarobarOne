import { apiGet, apiPatch, apiPost } from "./api-client";

/** Mirrors app.schemas.websiteSetting.WebsiteSettingResponse. */
export type WebsiteSettingResponse = {
  id: string;
  storeId: string;
  siteTitle: string | null;
  siteDescription: string | null;
  faviconMediaId: string | null;
  maintenanceMode: boolean;
  isPublic: boolean;
  createdAt: string;
  updatedAt: string;
};

/** Mirrors app.schemas.websiteSetting.WebsiteSettingCreate. */
export type WebsiteSettingCreateInput = {
  storeId: string;
  siteTitle?: string;
  siteDescription?: string;
  faviconMediaId?: string;
  maintenanceMode?: boolean;
  isPublic?: boolean;
};

/** Mirrors app.schemas.websiteSetting.WebsiteSettingUpdate — every field optional, PATCH-style. */
export type WebsiteSettingUpdateInput = Partial<{
  siteTitle: string;
  siteDescription: string;
  faviconMediaId: string;
  maintenanceMode: boolean;
  isPublic: boolean;
}>;

export const getStoreSettings = (storeId: string) =>
  apiGet<WebsiteSettingResponse>(`/website-settings/store/${storeId}`);

export const createStoreSettings = (input: WebsiteSettingCreateInput) =>
  apiPost<WebsiteSettingResponse>("/website-settings/", input);

export const updateStoreSettings = (storeId: string, input: WebsiteSettingUpdateInput) =>
  apiPatch<WebsiteSettingResponse>(`/website-settings/store/${storeId}`, input);

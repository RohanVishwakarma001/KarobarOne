import { corePost } from "./coreClient";

export type TenantCreate = {
  gstNumber?: string;
  panNumber: string;
  documentMediaLink?: string;
  documentVerificationDone?: boolean;
  businessName: string;
  legalName: string;
  email: string;
  mobile: string;
  whatsappMobile?: string;
  ownerName: string;
  businessAddressLine1: string;
  businessAddressLine2?: string;
  landmark?: string;
  city: string;
  state: string;
  country?: string;
  postalCode: string;
  businessType: string;
  businessDescription?: string;
  employeeCount?: number;
};

export type TenantRead = {
  id: string;
  businessName: string;
  legalName: string;
  email: string;
  mobile: string;
  city: string;
  state: string;
  businessType: string;
  isActive: boolean;
};

export type TenantRegistrationResponse = {
  tenant: TenantRead;
  accessToken: string | null;
  refreshToken: string | null;
  tokenType: string;
};

export const registerTenant = (data: TenantCreate) =>
  corePost<TenantRegistrationResponse>("/tenants", data);

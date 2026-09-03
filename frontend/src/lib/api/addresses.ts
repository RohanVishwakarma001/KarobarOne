import { apiPost } from "./api-client";

/** Mirrors app.schemas.customers.CustomerAddressCreate/Response (app/api/v1/endpoints/customerAddresses.py — ACTIVE, prefix "/addresses"). */
export type AddressCreateInput = {
  customerId: string;
  addressType: "SHIPPING" | "BILLING";
  fullName: string;
  mobile: string;
  addressLine1: string;
  addressLine2?: string;
  city: string;
  state: string;
  country?: string;
  postalCode: string;
  isDefault?: boolean;
};

export type AddressResponse = AddressCreateInput & {
  id: string;
  createdAt: string | null;
  updatedAt: string | null;
};

export const createAddress = (input: AddressCreateInput) => apiPost<AddressResponse>("/addresses/", input, { auth: false, tenant: false });

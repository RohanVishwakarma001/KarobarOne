import { apiDelete, apiGet, apiPatch, apiPost } from "./api-client";

/** Mirrors app.schemas.customers.CustomerAddressCreate/Response (app/api/v1/endpoints/customerAddresses.py — ACTIVE, prefix "/addresses"). */
export type AddressType = "SHIPPING" | "BILLING";

export type AddressCreateInput = {
  customerId: string;
  addressType: AddressType;
  fullName: string;
  mobile: string;
  addressLine1: string;
  addressLine2?: string;
  landmark?: string;
  city: string;
  state: string;
  country?: string;
  postalCode: string;
  isDefault?: boolean;
};

export type AddressUpdateInput = Partial<Omit<AddressCreateInput, "customerId">>;

export type AddressResponse = AddressCreateInput & {
  id: string;
  createdAt: string | null;
  updatedAt: string | null;
};

export const createAddress = (input: AddressCreateInput) =>
  apiPost<AddressResponse>("/addresses/", input, { auth: false, tenant: false });

export const listCustomerAddresses = (customerId: string) =>
  apiGet<AddressResponse[]>(`/addresses/customer/${customerId}`, { auth: false, tenant: false });

export const getAddress = (addressId: string) =>
  apiGet<AddressResponse>(`/addresses/${addressId}`, { auth: false, tenant: false });

export const updateAddress = (addressId: string, input: AddressUpdateInput) =>
  apiPatch<AddressResponse>(`/addresses/${addressId}`, input, { auth: false, tenant: false });

export const deleteAddress = (addressId: string) =>
  apiDelete<void>(`/addresses/${addressId}`, { auth: false, tenant: false });

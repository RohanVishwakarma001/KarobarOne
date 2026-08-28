import { ApiError, apiGet, apiPost, apiPut, apiDelete } from "../client";
import { TENANT_ID, assertStoreConfig } from "../config";

// ---------------------------------------------------------------------------
// Shipping Profiles
// ---------------------------------------------------------------------------

export interface ShippingProfile {
  id: string;
  tenant_id: string;
  profile_name: string;
  description?: string | null;
  free_shipping_threshold?: number | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
export function createShippingProfile(input: { profile_name: string; description?: string; free_shipping_threshold?: number; is_active?: boolean }) {
  assertStoreConfig();
  return apiPost<ShippingProfile>("/shipping-profiles/", { tenant_id: TENANT_ID, is_active: true, ...input });
}
export const listShippingProfiles = () => apiGet<ShippingProfile[]>("/shipping-profiles/");
export const getShippingProfile = (profileId: string) => apiGet<ShippingProfile>(`/shipping-profiles/${profileId}`);
export const updateShippingProfile = (
  profileId: string,
  data: Partial<Pick<ShippingProfile, "profile_name" | "description" | "free_shipping_threshold" | "is_active">>
) => apiPut<ShippingProfile>(`/shipping-profiles/${profileId}`, data);
export const deleteShippingProfile = (profileId: string) => apiDelete<void>(`/shipping-profiles/${profileId}`);

// ---------------------------------------------------------------------------
// Shipping Zones
// ---------------------------------------------------------------------------

export interface ShippingZone {
  id: string;
  tenant_id: string;
  zone_name: string;
  zone_code: string;
  country: string;
  state: string;
  city: string;
  postal_code_pattern?: string | null;
  is_active: boolean;
  created_at: string;
}
export function createShippingZone(input: {
  zone_name: string;
  zone_code: string;
  country: string;
  state: string;
  city: string;
  postal_code_pattern?: string;
  is_active?: boolean;
}) {
  assertStoreConfig();
  return apiPost<ShippingZone>("/shipping-zones/", { tenant_id: TENANT_ID, is_active: true, ...input });
}
export const listShippingZones = () => apiGet<ShippingZone[]>("/shipping-zones/");
export const getShippingZone = (zoneId: string) => apiGet<ShippingZone>(`/shipping-zones/${zoneId}`);
export const updateShippingZone = (
  zoneId: string,
  data: Partial<Pick<ShippingZone, "zone_name" | "country" | "state" | "city" | "postal_code_pattern" | "is_active">>
) => apiPut<ShippingZone>(`/shipping-zones/${zoneId}`, data);
export const deleteShippingZone = (zoneId: string) => apiDelete<void>(`/shipping-zones/${zoneId}`);

// ---------------------------------------------------------------------------
// Shipping Rates
// ---------------------------------------------------------------------------

export interface ShippingRate {
  id: string;
  shipping_profile_id: string;
  shipping_zone_id: string;
  minimum_weight: number;
  maximum_weight: number;
  shipping_charge: number;
  estimated_days_min: number;
  estimated_days_max: number;
  created_at: string;
}
export const createShippingRate = (input: Omit<ShippingRate, "id" | "created_at">) => apiPost<ShippingRate>("/shipping-rates/", input);
export const listShippingRates = () => apiGet<ShippingRate[]>("/shipping-rates/");
export const getShippingRate = (rateId: string) => apiGet<ShippingRate>(`/shipping-rates/${rateId}`);
export const updateShippingRate = (
  rateId: string,
  data: Partial<Pick<ShippingRate, "minimum_weight" | "maximum_weight" | "shipping_charge" | "estimated_days_min" | "estimated_days_max">>
) => apiPut<ShippingRate>(`/shipping-rates/${rateId}`, data);
export const deleteShippingRate = (rateId: string) => apiDelete<void>(`/shipping-rates/${rateId}`);

// ---------------------------------------------------------------------------
// Shipping Profile Zones (link table — create/read/delete only, no update route)
// ---------------------------------------------------------------------------

export interface ShippingProfileZone {
  id: string;
  shipping_profile_id: string;
  shipping_zone_id: string;
  created_at: string;
}
export const linkShippingProfileZone = (input: { shipping_profile_id: string; shipping_zone_id: string }) =>
  apiPost<ShippingProfileZone>("/shipping-profile-zones/", input);
export const listShippingProfileZones = () => apiGet<ShippingProfileZone[]>("/shipping-profile-zones/");
export const getShippingProfileZone = (id: string) => apiGet<ShippingProfileZone>(`/shipping-profile-zones/${id}`);
export const unlinkShippingProfileZone = (id: string) => apiDelete<void>(`/shipping-profile-zones/${id}`);

// ---------------------------------------------------------------------------
// Shipping Partners
// ---------------------------------------------------------------------------

export interface ShippingPartner {
  id: string;
  partner_code: string;
  partner_name: string;
  website_url?: string | null;
  tracking_url_template?: string | null;
  api_enabled: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
export const createShippingPartner = (input: {
  partner_code: string;
  partner_name: string;
  website_url?: string;
  tracking_url_template?: string;
  api_enabled?: boolean;
  is_active?: boolean;
}) => apiPost<ShippingPartner>("/shipping-partners/", { api_enabled: false, is_active: true, ...input });
export const listShippingPartners = () => apiGet<ShippingPartner[]>("/shipping-partners/");
export const getShippingPartner = (partnerId: string) => apiGet<ShippingPartner>(`/shipping-partners/${partnerId}`);
export const updateShippingPartner = (
  partnerId: string,
  data: Partial<Pick<ShippingPartner, "partner_name" | "website_url" | "tracking_url_template" | "api_enabled" | "is_active">>
) => apiPut<ShippingPartner>(`/shipping-partners/${partnerId}`, data);
export const deleteShippingPartner = (partnerId: string) => apiDelete<void>(`/shipping-partners/${partnerId}`);

// ---------------------------------------------------------------------------
// Shipments
// ---------------------------------------------------------------------------

export interface Shipment {
  id: string;
  order_id: string;
  shipment_request_id: string;
  shipping_partner_id: string;
  shipment_number?: string | null;
  tracking_number?: string | null;
  tracking_url?: string | null;
  shipment_status: string;
  shipped_at?: string | null;
  delivered_at?: string | null;
  created_at: string;
}
export const createShipment = (input: {
  order_id: string;
  shipping_partner_id: string;
  shipment_number: string;
  tracking_number?: string;
  tracking_url?: string;
  shipment_status?: string;
}) => apiPost<Shipment>("/shipments/", { shipment_status: "PENDING", ...input });
// No by-order filter server-side — fetch all and filter client-side.
export const listShipments = () => apiGet<Shipment[]>("/shipments/");
export const getShipment = (shipmentId: string) => apiGet<Shipment>(`/shipments/${shipmentId}`);
export const updateShipment = (
  shipmentId: string,
  data: Partial<Pick<Shipment, "shipment_number" | "tracking_number" | "tracking_url" | "shipment_status" | "shipped_at" | "delivered_at">>
) => apiPut<Shipment>(`/shipments/${shipmentId}`, data);
export const deleteShipment = (shipmentId: string) => apiDelete<void>(`/shipments/${shipmentId}`);

// ---------------------------------------------------------------------------
// Shipment Requests
// ---------------------------------------------------------------------------

export interface ShipmentRequest {
  id: string;
  order_id: string;
  /** Sic — backend response field is misspelled ("sshipping_profile_id"), not a typo here. */
  sshipping_profile_id?: string | null;
  request_status: string;
  requested_at: string;
  created_at: string;
}
export const createShipmentRequest = (input: { order_id: string; shipping_profile_id?: string; request_status?: string }) =>
  apiPost<ShipmentRequest>("/shipment-requests/", { request_status: "PENDING", ...input });
export const listShipmentRequests = () => apiGet<ShipmentRequest[]>("/shipment-requests/");
export const getShipmentRequest = (requestId: string) => apiGet<ShipmentRequest>(`/shipment-requests/${requestId}`);
export const updateShipmentRequest = (requestId: string, data: { request_status: string }) =>
  apiPut<ShipmentRequest>(`/shipment-requests/${requestId}`, data);
export const deleteShipmentRequest = (requestId: string) => apiDelete<void>(`/shipment-requests/${requestId}`);

// ---------------------------------------------------------------------------
// Shipping Exceptions
// ---------------------------------------------------------------------------

export interface ShippingException {
  id: string;
  shipment_id: string;
  exception_type: string;
  description?: string | null;
  resolved: boolean;
  resolved_at?: string | null;
  created_at: string;
}
export const createShippingException = (input: { shipment_id: string; exception_type: string; description?: string }) =>
  apiPost<ShippingException>("/shipping-exceptions/", input);
export const listShippingExceptions = () => apiGet<ShippingException[]>("/shipping-exceptions/");
export const getShippingException = (id: string) => apiGet<ShippingException>(`/shipping-exceptions/${id}`);
export const updateShippingException = (id: string, data: { exception_type?: string; description?: string; resolved?: boolean; resolved_at?: string }) =>
  apiPut<ShippingException>(`/shipping-exceptions/${id}`, data);
export const deleteShippingException = (id: string) => apiDelete<void>(`/shipping-exceptions/${id}`);

// ---------------------------------------------------------------------------
// Shiprocket — thin proxy over the third-party courier API, no local persistence.
// ---------------------------------------------------------------------------

async function proxyPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!res.ok) {
    let message = `Shiprocket request failed (${res.status})`;
    try {
      const body = await res.json();
      message = body?.error?.message ?? body?.detail ?? message;
    } catch {
      // ignore — keep the generic message
    }
    throw new ApiError(message, res.status);
  }
  return res.json();
}

export const shiprocketLogin = (input: { email: string; password: string }) => apiPost<{ token: string; [key: string]: unknown }>("/shiprocket/login", input);

export interface ShiprocketOrderItem {
  name: string;
  sku: string;
  units: number;
  selling_price: number;
}
export interface CreateShiprocketOrderInput {
  order_id: string;
  order_date: string;
  pickup_location: string;
  billing_customer_name: string;
  billing_address: string;
  billing_city: string;
  billing_pincode: string;
  billing_state: string;
  billing_country: string;
  billing_email: string;
  billing_phone: string;
  order_items: ShiprocketOrderItem[];
  payment_method: string;
  sub_total: number;
  length: number;
  breadth: number;
  height: number;
  weight: number;
  billing_last_name?: string;
  billing_address_2?: string;
  shipping_is_billing?: boolean;
  channel_id?: string;
}
export const createShiprocketOrder = (input: CreateShiprocketOrderInput) =>
  apiPost<{ success: boolean; data: Record<string, unknown> }>("/shiprocket/order", input);

export interface ServiceabilityRequest {
  pickup_postcode: string;
  delivery_postcode: string;
  weight: number;
  cod?: number;
}
/**
 * The backend route is `GET /shiprocket/serviceability` with a JSON body, which
 * fetch() cannot send on a GET — routed through our own server-side proxy instead.
 * See app/api/shiprocket/serviceability/route.ts.
 */
export const checkServiceability = (input: ServiceabilityRequest) =>
  proxyPost<Record<string, unknown>>("/api/shiprocket/serviceability", { cod: 0, ...input });

/** Same GET+body constraint as checkServiceability — see app/api/shiprocket/couriers/route.ts. */
export const getAvailableCouriers = (input: ServiceabilityRequest) =>
  proxyPost<Record<string, unknown>>("/api/shiprocket/couriers", { cod: 0, ...input });

export const generateAwb = (input: { shipment_id: number; courier_id: number }) => apiPost<Record<string, unknown>>("/shiprocket/awb", input);
export const requestPickup = (shipmentIds: number[]) => apiPost<Record<string, unknown>>("/shiprocket/pickup", { shipment_id: shipmentIds });
export const generateLabel = (shipmentIds: number[]) => apiPost<Record<string, unknown>>("/shiprocket/label", { shipment_id: shipmentIds });
export const generateShiprocketInvoice = (shipmentIds: number[]) => apiPost<Record<string, unknown>>("/shiprocket/invoice", { shipment_id: shipmentIds });
export const generateManifest = (shipmentIds: number[]) => apiPost<Record<string, unknown>>("/shiprocket/manifest", { shipment_id: shipmentIds });

export interface TrackingInfo {
  awb_code: string;
  current_status?: string;
  [key: string]: unknown;
}
export const trackShipment = (awbCode: string) => apiGet<TrackingInfo>(`/shiprocket/track/${awbCode}`);

export const cancelShiprocketOrders = (orderIds: number[]) => apiPost<Record<string, unknown>>("/shiprocket/cancel", orderIds);
export const listShiprocketOrders = () => apiGet<Record<string, unknown>>("/shiprocket/orders");
export const getShiprocketOrder = (orderId: number) => apiGet<Record<string, unknown>>(`/shiprocket/orders/${orderId}`);
export const updateShiprocketOrder = (input: { order_id: number; order_status: string }) =>
  apiPut<Record<string, unknown>>("/shiprocket/orders", input);

export const listPickupLocations = () => apiGet<Record<string, unknown>>("/shiprocket/pickup-locations");
export interface PickupLocationInput {
  pickup_location: string;
  name: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  pin_code: string;
  address_2?: string;
  country?: string;
}
export const addPickupLocation = (input: PickupLocationInput) =>
  apiPost<{ success: boolean; message: string }>("/shiprocket/pickup-location", { country: "India", address_2: "", ...input });

export const listShiprocketChannels = () => apiGet<Record<string, unknown>>("/shiprocket/channels");
export const listCourierCompanies = () => apiGet<Record<string, unknown>>("/shiprocket/courier-companies");
export const listNdrShipments = () => apiGet<Record<string, unknown>>("/shiprocket/ndr");
export const actOnNdrShipment = (input: { shipment_id: number; action: string; comments?: string }) =>
  apiPost<Record<string, unknown>>("/shiprocket/ndr", { comments: "", ...input });

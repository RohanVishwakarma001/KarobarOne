import { apiGet, apiPost, apiPut, apiDelete } from "../client";
import { TENANT_ID, STORE_ID, assertStoreConfig } from "../config";

export type OfferType = "PRODUCT" | "SERVICE" | "CATEGORY" | "STORE" | "COUPON";
export type OfferDiscountType = "PERCENTAGE" | "FLAT";
export type OfferApprovalStatus = "PENDING" | "APPROVED" | "REJECTED";

export interface Offer {
  id: string;
  tenant_id: string;
  store_id: string;
  offer_name: string;
  offer_code: string;
  offer_type: OfferType;
  discount_type: OfferDiscountType;
  discount_value: number;
  maximum_discount_amount?: number | null;
  minimum_order_amount?: number | null;
  starts_at: string;
  ends_at: string;
  priority?: number | null;
  is_active?: boolean | null;
  approval_status: OfferApprovalStatus;
  created_by: string;
  approved_by?: string | null;
  approved_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateOfferInput {
  offer_name: string;
  offer_code: string;
  offer_type: OfferType;
  discount_type: OfferDiscountType;
  discount_value: number;
  starts_at: string;
  ends_at: string;
  created_by: string;
  maximum_discount_amount?: number;
  minimum_order_amount?: number;
  priority?: number;
  is_active?: boolean;
}
export function createOffer(input: CreateOfferInput) {
  assertStoreConfig();
  return apiPost<Offer>("/offers/", { tenant_id: TENANT_ID, store_id: STORE_ID, is_active: true, ...input });
}
export const listOffers = () => apiGet<Offer[]>("/offers/");
export const getOffer = (offerId: string) => apiGet<Offer>(`/offers/${offerId}`);
export const updateOffer = (
  offerId: string,
  data: Partial<
    Pick<
      Offer,
      | "offer_name"
      | "offer_code"
      | "offer_type"
      | "discount_type"
      | "discount_value"
      | "maximum_discount_amount"
      | "minimum_order_amount"
      | "starts_at"
      | "ends_at"
      | "priority"
      | "is_active"
      | "approval_status"
      | "approved_by"
      | "approved_at"
    >
  >
) => apiPut<Offer>(`/offers/${offerId}`, data);
export const deleteOffer = (offerId: string) => apiDelete<void>(`/offers/${offerId}`);

// ---------------------------------------------------------------------------
// Offer Targets — what the offer applies to. Create/read/delete only.
// ---------------------------------------------------------------------------

export type OfferTargetType = "PRODUCT" | "SERVICE" | "CATEGORY" | "STORE";
export interface OfferTarget {
  id: string;
  offer_id: string;
  target_type: OfferTargetType;
  target_id: string;
  created_at?: string | null;
}
export const attachOfferTarget = (input: { offer_id: string; target_type: OfferTargetType; target_id: string }) =>
  apiPost<OfferTarget>("/offer-targets/", input);
export const listOfferTargets = () => apiGet<OfferTarget[]>("/offer-targets/");
export const getOfferTarget = (targetId: string) => apiGet<OfferTarget>(`/offer-targets/${targetId}`);
export const removeOfferTarget = (targetId: string) => apiDelete<void>(`/offer-targets/${targetId}`);

// ---------------------------------------------------------------------------
// Offer Customer Segments — restrict an offer to a customer group.
// ---------------------------------------------------------------------------

export interface OfferCustomerSegment {
  id: string;
  offer_id: string;
  customer_group_id: string;
  created_at: string;
}
export const createOfferCustomerSegment = (input: { offer_id: string; customer_group_id: string }) =>
  apiPost<OfferCustomerSegment>("/offer-customer-segments/", input);
export const listOfferCustomerSegments = () => apiGet<OfferCustomerSegment[]>("/offer-customer-segments/");
export const getOfferCustomerSegment = (segmentId: string) => apiGet<OfferCustomerSegment>(`/offer-customer-segments/${segmentId}`);
export const updateOfferCustomerSegment = (segmentId: string, data: Partial<Pick<OfferCustomerSegment, "offer_id" | "customer_group_id">>) =>
  apiPut<OfferCustomerSegment>(`/offer-customer-segments/${segmentId}`, data);
export const deleteOfferCustomerSegment = (segmentId: string) => apiDelete<void>(`/offer-customer-segments/${segmentId}`);

// ---------------------------------------------------------------------------
// Offer Exclusions — entities an offer explicitly does NOT apply to.
// ---------------------------------------------------------------------------

export type OfferExclusionEntityType = "PRODUCT" | "SERVICE" | "CATEGORY" | "CUSTOMER_GROUP";
export interface OfferExclusion {
  id: string;
  offer_id: string;
  entity_type: OfferExclusionEntityType;
  entity_id: string;
  created_at: string;
}
export const createOfferExclusion = (input: { offer_id: string; entity_type: OfferExclusionEntityType; entity_id: string }) =>
  apiPost<OfferExclusion>("/offer-exclusions/", input);
export const listOfferExclusions = () => apiGet<OfferExclusion[]>("/offer-exclusions/");
export const getOfferExclusion = (exclusionId: string) => apiGet<OfferExclusion>(`/offer-exclusions/${exclusionId}`);
export const updateOfferExclusion = (exclusionId: string, data: Partial<Pick<OfferExclusion, "offer_id" | "entity_type" | "entity_id">>) =>
  apiPut<OfferExclusion>(`/offer-exclusions/${exclusionId}`, data);
export const deleteOfferExclusion = (exclusionId: string) => apiDelete<void>(`/offer-exclusions/${exclusionId}`);

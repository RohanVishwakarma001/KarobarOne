import { apiGet, apiPost, apiDelete } from "../client";
import { STORE_ID, assertStoreConfig } from "../config";

export interface ProductCompareList {
  id: string;
  customer_id: string;
  store_id: string;
  created_at?: string;
}

export interface ProductCompareItem {
  id: string;
  compare_list_id: string;
  product_id: string;
  added_at?: string;
}

export interface RecentlyViewedProduct {
  id: string;
  customer_id: string;
  product_id: string;
  viewed_at?: string;
}

export function createCompareList(customerId: string) {
  assertStoreConfig();
  return apiPost<ProductCompareList>("/product-compare-lists/", { customer_id: customerId, store_id: STORE_ID });
}
export const listCompareLists = () => apiGet<ProductCompareList[]>("/product-compare-lists/");
export const deleteCompareList = (compareListId: string) => apiDelete<void>(`/product-compare-lists/${compareListId}`);

export const addCompareItem = (input: { compare_list_id: string; product_id: string }) =>
  apiPost<ProductCompareItem>("/product-compare-items/", input);
export const listCompareItems = () => apiGet<ProductCompareItem[]>("/product-compare-items/");
export const removeCompareItem = (compareItemId: string) => apiDelete<void>(`/product-compare-items/${compareItemId}`);

export const recordRecentlyViewed = (input: { customer_id: string; product_id: string }) =>
  apiPost<RecentlyViewedProduct>("/recently-viewed-products/", input);
export const listRecentlyViewed = () => apiGet<RecentlyViewedProduct[]>("/recently-viewed-products/");

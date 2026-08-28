import { apiGet, apiPost, apiDelete, apiPut } from "../client";
import { STORE_ID, assertStoreConfig } from "../config";

export interface Wishlist {
  id: string;
  customer_id: string;
  store_id: string;
  wishlist_name: string;
  is_default: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface WishlistItem {
  id: string;
  wishlist_id: string;
  product_id: string;
  product_variant_id?: string | null;
  added_at?: string;
}

export interface SavedForLaterItem {
  id: string;
  customer_id: string;
  product_id: string;
  product_variant_id?: string | null;
  quantity: number;
  added_at?: string;
}

export function createWishlist(customerId: string, name = "My Wishlist") {
  assertStoreConfig();
  return apiPost<Wishlist>("/wishlists/", { customer_id: customerId, store_id: STORE_ID, wishlist_name: name, is_default: true });
}
// No by-customer filter server-side — list all and filter client-side, or cache the wishlistId.
export const listWishlists = () => apiGet<Wishlist[]>("/wishlists/");
export const deleteWishlist = (wishlistId: string) => apiDelete<void>(`/wishlists/${wishlistId}`);

export const addWishlistItem = (input: { wishlist_id: string; product_id: string; product_variant_id?: string }) =>
  apiPost<WishlistItem>("/wishlist-items/", input);
export const listWishlistItems = () => apiGet<WishlistItem[]>("/wishlist-items/");
export const removeWishlistItem = (wishlistItemId: string) => apiDelete<void>(`/wishlist-items/${wishlistItemId}`);

export const addSavedForLater = (input: { customer_id: string; product_id: string; product_variant_id?: string; quantity?: number }) =>
  apiPost<SavedForLaterItem>("/saved-for-later/", { quantity: 1, ...input });
export const listSavedForLater = () => apiGet<SavedForLaterItem[]>("/saved-for-later/");
export const updateSavedForLaterQty = (id: string, quantity: number) => apiPut<SavedForLaterItem>(`/saved-for-later/${id}`, { quantity });
export const removeSavedForLater = (id: string) => apiDelete<void>(`/saved-for-later/${id}`);

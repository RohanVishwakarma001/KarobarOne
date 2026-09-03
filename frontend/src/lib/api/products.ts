import { apiDelete, apiGet, apiPatch } from "./api-client";

/** Mirrors app.productsPorted.schemas.schemas.ProductResponse (top-level fields only — nested relations omitted here, see variants.ts for VariantResponse). */
export type ProductResponse = {
  id: string;
  tenantId: string;
  storeId: string;
  name: string;
  slug: string;
  description: string | null;
  status: "DRAFT" | "PENDING" | "PUBLISHED" | "ARCHIVED" | "ACTIVE";
  productType: "PHYSICAL" | "DIGITAL";
  sku: string | null;
  metaTitle: string | null;
  metaDescription: string | null;
  categoryId: string | null;
  brandId: string | null;
  shippingProfileId: string | null;
  createdAt: string | null;
  updatedAt: string | null;
  deletedAt: string | null;
};

/** Mirrors app.productsPorted.schemas.schemas.ProductUpdate — every field optional, PATCH-style. */
export type ProductUpdateInput = Partial<{
  name: string;
  slug: string;
  description: string;
  status: ProductResponse["status"];
  productType: ProductResponse["productType"];
  sku: string;
  metaTitle: string;
  metaDescription: string;
  categoryId: string;
  brandId: string;
  shippingProfileId: string;
}>;

export const getProduct = (productId: string) => apiGet<ProductResponse>(`/catalog/products/${productId}`);

export const updateProduct = (productId: string, input: ProductUpdateInput) =>
  apiPatch<ProductResponse>(`/catalog/products/${productId}`, input);

/** 204 No Content — app/productsPorted/routers/products.py::delete_product (soft delete). */
export const deleteProduct = (productId: string) => apiDelete<void>(`/catalog/products/${productId}`);

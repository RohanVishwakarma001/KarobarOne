import { coreDelete, coreGet, corePost, corePut, withTenant } from "./coreClient";

/** Mirrors app.productsPorted.schemas.schemas.VariantResponse exactly. */
export type VariantResponse = {
  id: string;
  productId: string;
  tenantId: string | null;
  sku: string;
  price: number;
  inventory: number;
  attributes: Record<string, string> | null;
  createdAt: string | null;
  updatedAt: string | null;
  deletedAt: string | null;
};

/** Mirrors app.productsPorted.schemas.schemas.VariantCreateForProduct — productId/tenantId come from the URL/header, not the body. */
export type VariantCreateForProductInput = {
  sku: string;
  price: number;
  inventory: number;
  attributes: Record<string, string> | null;
};

/** Mirrors app.productsPorted.schemas.schemas.ProductImageResponse. */
export type ProductImageResponse = {
  id: string;
  productId: string;
  variantId: string | null;
  url: string;
  altText: string | null;
  isPrimary: boolean;
  fileSize: number;
  fileType: string;
  createdAt: string | null;
  updatedAt: string | null;
};

/**
 * GET /api/v1/catalog/products/{productId}/variants
 * (app/productsPorted/routers/variants.py::list_variants_for_product)
 */
export function listProductVariants(productId: string): Promise<VariantResponse[]> {
  return coreGet<VariantResponse[]>(`/catalog/products/${productId}/variants`);
}

/**
 * POST /api/v1/catalog/products/{productId}/variants — requires X-Tenant-ID;
 * the backend 403s if the product belongs to a different tenant, and 409s on
 * a SKU already used anywhere in this tenant's catalog, and 400s on a
 * duplicate {axis: value} combination for the same product.
 */
export function createProductVariant(
  productId: string,
  tenantId: string,
  input: VariantCreateForProductInput,
): Promise<VariantResponse> {
  return corePost<VariantResponse>(`/catalog/products/${productId}/variants`, input, true, withTenant(tenantId));
}

/** PUT /api/v1/catalog/products/{productId}/variants/{variantId} — full replace. */
export function replaceProductVariant(
  productId: string,
  variantId: string,
  input: VariantCreateForProductInput,
): Promise<VariantResponse> {
  return corePut<VariantResponse>(`/catalog/products/${productId}/variants/${variantId}`, input);
}

/** DELETE /api/v1/catalog/products/{productId}/variants/{variantId} — 204 No Content. */
export function deleteProductVariant(productId: string, variantId: string): Promise<void> {
  return coreDelete<void>(`/catalog/products/${productId}/variants/${variantId}`);
}

/**
 * POST /api/v1/catalog/images/upload (multipart) — attaches to one variant
 * when variantId is given, otherwise to the whole product.
 */
export function uploadVariantImage(params: {
  productId: string;
  variantId?: string;
  file: File;
  isPrimary?: boolean;
}): Promise<ProductImageResponse> {
  const form = new FormData();
  form.append("productId", params.productId);
  if (params.variantId) form.append("variantId", params.variantId);
  form.append("isPrimary", String(params.isPrimary ?? false));
  form.append("file", params.file);

  // multipart bodies must not get the client's default "Content-Type: application/json" —
  // let fetch set its own boundary-including content-type, so this bypasses coreRequest's JSON path.
  return fetch(
    `${process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000"}/api/v1/catalog/images/upload`,
    { method: "POST", body: form },
  ).then(async (res) => {
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      const message = body?.error?.message ?? body?.detail ?? `Upload failed (${res.status})`;
      throw new Error(message);
    }
    return res.json() as Promise<ProductImageResponse>;
  });
}

export function listVariantImages(productId: string, variantId: string): Promise<ProductImageResponse[]> {
  return coreGet<ProductImageResponse[]>(`/catalog/images/?productId=${productId}&variantId=${variantId}`);
}

/** DELETE /api/v1/catalog/images/{imageId} — 204 No Content (app/productsPorted/routers/images.py::delete_image). */
export function deleteVariantImage(imageId: string): Promise<void> {
  return coreDelete<void>(`/catalog/images/${imageId}`);
}

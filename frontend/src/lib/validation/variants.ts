import { z } from "zod";

/**
 * One matrix row — matches app.productsPorted.schemas.schemas.VariantCreateForProduct
 * (sku, price, inventory, attributes) plus client-only bookkeeping fields
 * (clientId for React keys / useFieldArray, variantId once persisted).
 */
export const variantRowSchema = z.object({
  clientId: z.string(),
  variantId: z.string().optional(),
  sku: z.string().trim().min(1, "SKU is required").max(100, "Keep it under 100 characters"),
  price: z.coerce.number({ invalid_type_error: "Enter a price" }).min(0, "Price must be 0 or more"),
  inventory: z.coerce
    .number({ invalid_type_error: "Enter a stock count" })
    .int("Whole numbers only")
    .min(0, "Stock must be 0 or more"),
  attributes: z.record(z.string(), z.string()),
});
export type VariantRowValues = z.infer<typeof variantRowSchema>;

function attributesEqual(a: Record<string, string>, b: Record<string, string>): boolean {
  const aKeys = Object.keys(a);
  const bKeys = Object.keys(b);
  if (aKeys.length !== bKeys.length) return false;
  return aKeys.every((k) => a[k] === b[k]);
}

/**
 * The array-level schema — flags duplicate SKUs and duplicate attribute
 * combinations client-side before they hit the backend's 409/400 checks
 * (app/productsPorted/routers/variants.py::_assertSkuAvailable /
 * _assertNoDuplicateAttributeCombo), so the merchant sees the problem inline
 * instead of via a toast after submit.
 */
export const variantMatrixSchema = z.object({
  rows: z.array(variantRowSchema).superRefine((rows, ctx) => {
    rows.forEach((row, index) => {
      const dupSkuIndex = rows.findIndex((r, i) => i !== index && r.sku.trim().toLowerCase() === row.sku.trim().toLowerCase());
      if (dupSkuIndex !== -1 && dupSkuIndex < index) {
        ctx.addIssue({ code: "custom", message: `Duplicate SKU "${row.sku}"`, path: [index, "sku"] });
      }
      const dupComboIndex = rows.findIndex((r, i) => i !== index && attributesEqual(r.attributes, row.attributes));
      if (dupComboIndex !== -1 && dupComboIndex < index) {
        ctx.addIssue({ code: "custom", message: "Duplicate attribute combination", path: [index, "sku"] });
      }
    });
  }),
});
export type VariantMatrixValues = z.infer<typeof variantMatrixSchema>;

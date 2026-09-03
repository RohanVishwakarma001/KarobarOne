import { z } from "zod";
import { CUSTOMER_STATUSES } from "@/lib/api/customers";

/** Empty-string form fields become `undefined` rather than "" before validation/submit. */
function optionalTrimmed(max: number) {
  return z.preprocess(
    (v) => (typeof v === "string" && v.trim() === "" ? undefined : v),
    z.string().trim().max(max, `Keep it under ${max} characters`).optional(),
  );
}

/**
 * Shared fields between create and edit — matches
 * app/schemas/customers.py CustomerBase exactly (tenantId/storeId are
 * injected from session/store context, never user-typed, so they're
 * intentionally excluded from the form schema).
 */
const baseCustomerFields = {
  firstName: z.string().trim().min(1, "First name is required").max(100, "Keep it under 100 characters"),
  lastName: optionalTrimmed(100),
  email: z.string().trim().min(1, "Email is required").max(255, "Keep it under 255 characters").email("Enter a valid email address"),
  mobile: z
    .string()
    .trim()
    .min(7, "Enter a valid mobile number")
    .max(15, "Enter a valid mobile number")
    .regex(/^\+?[0-9]{7,15}$/, "Digits only, optionally starting with +"),
  status: z.enum(CUSTOMER_STATUSES),
  isGuestCustomer: z.boolean(),
  isEmailVerified: z.boolean(),
  isMobileVerified: z.boolean(),
};

/** Matches app.schemas.customers.CustomerCreate (password is create-only). */
export const customerCreateSchema = z.object({
  ...baseCustomerFields,
  password: optionalTrimmed(72), // bcrypt truncates/errors past 72 bytes
});
export type CustomerCreateFormValues = z.infer<typeof customerCreateSchema>;

/** Matches app.schemas.customers.CustomerUpdate — that schema has no password field. */
export const customerUpdateSchema = z.object(baseCustomerFields);
export type CustomerUpdateFormValues = z.infer<typeof customerUpdateSchema>;

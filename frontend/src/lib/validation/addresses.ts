import { z } from "zod";

/** Matches app.schemas.customers.CustomerAddressBase's field_validator exactly. */
export const ADDRESS_TYPES = ["SHIPPING", "BILLING"] as const;

export const addressFormSchema = z.object({
  addressType: z.enum(ADDRESS_TYPES),
  fullName: z.string().trim().min(1, "Full name is required").max(150),
  mobile: z.string().trim().min(7, "Enter a valid mobile number").max(15),
  addressLine1: z.string().trim().min(1, "Address is required").max(255),
  addressLine2: z.string().trim().max(255).optional(),
  landmark: z.string().trim().max(255).optional(),
  city: z.string().trim().min(1, "City is required").max(100),
  state: z.string().trim().min(1, "State is required").max(100),
  postalCode: z
    .string()
    .trim()
    .regex(/^[0-9]{4,10}$/, "Enter a valid postal code"),
  isDefault: z.boolean(),
});

export type AddressFormValues = z.infer<typeof addressFormSchema>;

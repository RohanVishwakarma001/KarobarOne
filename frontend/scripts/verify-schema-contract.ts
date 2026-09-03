/**
 * Quick contract check: does each Zod form schema (source of truth for what
 * the UI sends) still match the FastAPI/Pydantic model it's meant to satisfy
 * (source of truth for what the backend accepts)?
 *
 * Reads a static openapi.json (generate it with
 * `python backend/scripts/export_openapi.py backend/openapi.json`) rather
 * than hitting a live server — deterministic, no server process needed in CI.
 *
 * This is a drift *detector*, not a full structural-equality checker: field
 * *names* and *required-ness* are compared; it does not attempt to prove
 * the value types line up (Zod's `z.coerce.number()` vs Pydantic's `float`
 * aren't directly comparable at this level; a mismatch there would show up
 * as a 422 in the contract tests instead — see backend/tests/test_*_contract.py).
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";

import { customerCreateSchema, customerUpdateSchema } from "../src/lib/validation/customers";
import { variantRowSchema } from "../src/lib/validation/variants";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

type ContractCheck = {
  label: string;
  zodSchema: z.ZodObject<z.ZodRawShape>;
  openApiComponent: string;
  /** Fields the backend model has that the frontend deliberately doesn't collect (injected from session/URL/server defaults, not user input). */
  serverInjectedFields?: string[];
};

const CHECKS: ContractCheck[] = [
  {
    label: "Customer create (POST /customers/)",
    zodSchema: customerCreateSchema,
    openApiComponent: "app__schemas__customers__CustomerCreate",
    // tenantId/storeId come from session/store context (see create-customer-dialog.tsx),
    // customerCode is server-generated if omitted (see customers.py::createCustomer).
    serverInjectedFields: ["tenantId", "storeId", "customerCode"],
  },
  {
    label: "Customer update (PATCH /customers/{id})",
    zodSchema: customerUpdateSchema,
    openApiComponent: "app__schemas__customers__CustomerUpdate",
  },
  {
    label: "Variant create (POST /catalog/products/{id}/variants)",
    zodSchema: variantRowSchema.omit({ clientId: true, variantId: true }),
    openApiComponent: "VariantCreateForProduct",
  },
];

function isZodFieldRequired(fieldSchema: z.ZodTypeAny): boolean {
  // Zod v3: optional()/default()/nullable() wrappers all mean "the caller
  // doesn't have to supply this" from the API-contract's point of view.
  return !(
    fieldSchema.isOptional() ||
    fieldSchema instanceof z.ZodDefault ||
    fieldSchema instanceof z.ZodNullable
  );
}

type OpenApiSchemaNode = {
  properties?: Record<string, unknown>;
  required?: string[];
};

function loadOpenApiComponent(openapi: { components?: { schemas?: Record<string, OpenApiSchemaNode> } }, name: string): OpenApiSchemaNode {
  const schema = openapi.components?.schemas?.[name];
  if (!schema) {
    const available = Object.keys(openapi.components?.schemas ?? {}).filter((k) => k.toLowerCase().includes(name.split("__").pop()!.toLowerCase().slice(0, 6)));
    throw new Error(
      `Component "${name}" not found in openapi.json. Similarly-named components present: ${available.join(", ") || "(none)"}`,
    );
  }
  return schema;
}

function runCheck(check: ContractCheck, openapi: Parameters<typeof loadOpenApiComponent>[0]): { ok: boolean; lines: string[] } {
  const lines: string[] = [];
  let ok = true;

  const pydantic = loadOpenApiComponent(openapi, check.openApiComponent);
  const pydanticFields = new Set(Object.keys(pydantic.properties ?? {}));
  const pydanticRequired = new Set(pydantic.required ?? []);

  const zodShape = check.zodSchema.shape;
  const zodFields = new Set(Object.keys(zodShape));
  const ignored = new Set(check.serverInjectedFields ?? []);

  const missingInZod = [...pydanticFields].filter((f) => !zodFields.has(f) && !ignored.has(f));
  const extraInZod = [...zodFields].filter((f) => !pydanticFields.has(f));
  const staleIgnores = [...ignored].filter((f) => !pydanticFields.has(f));

  if (missingInZod.length > 0) {
    ok = false;
    lines.push(`  ✗ Backend has fields the Zod schema never sends: ${missingInZod.join(", ")}`);
  }
  if (extraInZod.length > 0) {
    ok = false;
    lines.push(`  ✗ Zod schema sends fields the backend model doesn't declare: ${extraInZod.join(", ")}`);
  }
  if (staleIgnores.length > 0) {
    ok = false;
    lines.push(`  ✗ serverInjectedFields lists fields no longer on the backend model (stale mapping): ${staleIgnores.join(", ")}`);
  }

  const requiredMismatches: string[] = [];
  for (const field of zodFields) {
    if (!pydanticFields.has(field)) continue;
    const zodRequired = isZodFieldRequired(zodShape[field]);
    const pydanticRequiredHere = pydanticRequired.has(field);
    if (zodRequired !== pydanticRequiredHere) {
      requiredMismatches.push(`${field} (zod: ${zodRequired ? "required" : "optional"}, backend: ${pydanticRequiredHere ? "required" : "optional"})`);
    }
  }
  if (requiredMismatches.length > 0) {
    // Warning-level, not fatal: e.g. Zod enforcing stricter client-side UX
    // (required in the form) than the backend (optional there) is often intentional.
    lines.push(`  ⚠ required-ness differs: ${requiredMismatches.join("; ")}`);
  }

  if (ok && requiredMismatches.length === 0) {
    lines.push("  ✓ field names and required-ness match");
  }

  return { ok, lines };
}

function main() {
  const openapiPath = process.argv[2] ?? path.resolve(__dirname, "../../backend/openapi.json");
  if (!fs.existsSync(openapiPath)) {
    console.error(`openapi.json not found at ${openapiPath}`);
    console.error("Generate it with: cd backend && python scripts/export_openapi.py openapi.json");
    process.exit(2);
  }
  const openapi = JSON.parse(fs.readFileSync(openapiPath, "utf-8"));

  console.log(`Schema contract check against ${openapiPath}\n`);

  let allOk = true;
  for (const check of CHECKS) {
    console.log(check.label);
    try {
      const { ok, lines } = runCheck(check, openapi);
      lines.forEach((l) => console.log(l));
      allOk = allOk && ok;
    } catch (err) {
      allOk = false;
      console.log(`  ✗ ${err instanceof Error ? err.message : String(err)}`);
    }
    console.log("");
  }

  if (!allOk) {
    console.error("Contract check FAILED — a Zod schema and its Pydantic model have drifted apart.");
    process.exit(1);
  }
  console.log("Contract check passed.");
}

main();

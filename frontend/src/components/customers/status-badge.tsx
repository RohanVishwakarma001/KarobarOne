import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { CUSTOMER_STATUSES, type CustomerStatus } from "@/lib/api/customers";

type StatusStyle = { label: string; className: string };

/**
 * `satisfies Record<CustomerStatus, StatusStyle>` makes this exhaustive at
 * compile time — if CUSTOMER_STATUSES (lib/api/customers.ts, mirroring the
 * backend's field_validator) ever gains a value, this object literal stops
 * type-checking until a style is added for it. No default/fallback branch
 * needed at the call site.
 */
const STATUS_STYLES = {
  ACTIVE: { label: "Active", className: "bg-emerald-50 text-emerald-700 border-emerald-200" },
  INACTIVE: { label: "Inactive", className: "bg-slate-100 text-slate-600 border-slate-200" },
  BLOCKED: { label: "Blocked", className: "bg-red-50 text-red-700 border-red-200" },
} satisfies Record<CustomerStatus, StatusStyle>;

// Compile-time exhaustiveness guard: fails to build if a status is missing above.
CUSTOMER_STATUSES satisfies readonly (keyof typeof STATUS_STYLES)[];

export function CustomerStatusBadge({ status, className }: { status: CustomerStatus; className?: string }) {
  const style = STATUS_STYLES[status];
  return <Badge variant="outline" className={cn(style.className, className)}>{style.label}</Badge>;
}

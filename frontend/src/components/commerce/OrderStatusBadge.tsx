import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { OrderStatus } from "@/lib/api/commerce";

type StatusStyle = { label: string; className: string };

/** `satisfies Record<OrderStatus, ...>` — exhaustive at compile time, same pattern as CustomerStatusBadge. */
const STATUS_STYLES = {
  PENDING: { label: "Pending", className: "bg-amber-50 text-amber-700 border-amber-200" },
  PAID: { label: "Paid", className: "bg-sky-50 text-sky-700 border-sky-200" },
  PROCESSING: { label: "Processing", className: "bg-indigo-50 text-indigo-700 border-indigo-200" },
  SHIPPED: { label: "Shipped", className: "bg-violet-50 text-violet-700 border-violet-200" },
  DELIVERED: { label: "Delivered", className: "bg-emerald-50 text-emerald-700 border-emerald-200" },
  CANCELLED: { label: "Cancelled", className: "bg-red-50 text-red-700 border-red-200" },
} satisfies Record<OrderStatus, StatusStyle>;

export function OrderStatusBadge({ status, className }: { status: OrderStatus; className?: string }) {
  const style = STATUS_STYLES[status];
  return <Badge variant="outline" className={cn(style.className, className)}>{style.label}</Badge>;
}

"use client";

import { motion } from "framer-motion";
import { Check, PackageX } from "lucide-react";
import { cn } from "@/lib/utils";
import type { StatusHistoryEvent } from "@/lib/api/statusHistory";
import { useReducedMotion } from "@/lib/motion";

/** Matches SHIPROCKET_STATUS_MAP's canonical values in app/api/v1/endpoints/github/shiprocketRouter.py::shiprocketWebhook. */
const SHIPMENT_STEPS = ["ORDERED", "PACKED", "IN_TRANSIT", "OUT_FOR_DELIVERY", "DELIVERED"] as const;

const STEP_LABELS: Record<(typeof SHIPMENT_STEPS)[number], string> = {
  ORDERED: "Ordered",
  PACKED: "Packed",
  IN_TRANSIT: "In transit",
  OUT_FOR_DELIVERY: "Out for delivery",
  DELIVERED: "Delivered",
};

function formatWhen(iso: string | null): string {
  if (!iso) return "";
  return new Date(iso).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" });
}

/**
 * Animated step tracker for a shipment's Shiprocket-driven tracking history
 * (GET /api/v1/status-history/?entityType=SHIPMENT&entityId=...), populated
 * by the webhook in shiprocketRouter.py — not the order-level PENDING/PAID/
 * PROCESSING/SHIPPED/DELIVERED state machine OrderTimeline.tsx renders.
 */
export function ShipmentTimeline({ currentStatus, history }: { currentStatus: string; history: StatusHistoryEvent[] }) {
  const reducedMotion = useReducedMotion();

  if (currentStatus === "CANCELLED" || currentStatus === "RTO") {
    const terminalEvent = history.find((h) => h.newStatus === currentStatus);
    return (
      <div className="flex items-center gap-3 rounded-2xl border border-red-100 bg-red-50/60 p-4">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-red-100 text-red-600">
          <PackageX className="h-4 w-4" />
        </div>
        <div>
          <p className="font-medium text-red-700">{currentStatus === "RTO" ? "Returned to origin" : "Shipment cancelled"}</p>
          <p className="text-xs text-red-400">{formatWhen(terminalEvent?.changedAt ?? null)}</p>
        </div>
      </div>
    );
  }

  const currentIndex = SHIPMENT_STEPS.indexOf(currentStatus as (typeof SHIPMENT_STEPS)[number]);
  const eventByStatus = new Map(history.map((h) => [h.newStatus, h]));

  return (
    <ol className="relative flex flex-col sm:flex-row sm:items-start sm:justify-between">
      {SHIPMENT_STEPS.map((step, index) => {
        const isDone = index <= currentIndex;
        const isCurrent = index === currentIndex;
        const event = eventByStatus.get(step);
        const isLast = index === SHIPMENT_STEPS.length - 1;

        return (
          <li key={step} className="relative flex flex-1 items-start gap-3 pb-6 sm:flex-col sm:items-center sm:gap-2 sm:pb-0 sm:text-center">
            {!isLast && (
              <span
                className={cn(
                  "absolute left-[15px] top-8 h-full w-px sm:left-1/2 sm:top-4 sm:h-px sm:w-full",
                  isDone ? "bg-[#5b4ef9]" : "bg-slate-200",
                )}
                aria-hidden
              />
            )}
            <motion.div
              initial={reducedMotion ? { opacity: 0 } : { opacity: 0, scale: 0.6 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: reducedMotion ? 0 : index * 0.06, type: "spring", stiffness: 400, damping: 24 }}
              className={cn(
                "z-10 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2",
                isDone ? "border-[#5b4ef9] bg-[#5b4ef9] text-white" : "border-slate-200 bg-white text-slate-300",
                isCurrent && !reducedMotion && "ring-4 ring-[#5b4ef9]/15",
              )}
            >
              {isDone ? <Check className="h-4 w-4" /> : <span className="h-2 w-2 rounded-full bg-current" />}
            </motion.div>
            <div className="pt-0.5 sm:pt-1">
              <p className={cn("text-sm font-medium", isDone ? "text-slate-900" : "text-slate-400")}>{STEP_LABELS[step]}</p>
              {event && <p className="text-xs text-slate-400">{formatWhen(event.changedAt)}</p>}
            </div>
          </li>
        );
      })}
    </ol>
  );
}

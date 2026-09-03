"use client";

import { motion } from "framer-motion";
import { Check, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { ORDER_STATUS_SEQUENCE, type OrderStatus, type OrderStatusEvent } from "@/lib/api/commerce";
import { useReducedMotion } from "@/lib/motion";

const STEP_LABELS: Record<(typeof ORDER_STATUS_SEQUENCE)[number], string> = {
  PENDING: "Order placed",
  PAID: "Payment confirmed",
  PROCESSING: "Preparing your order",
  SHIPPED: "Shipped",
  DELIVERED: "Delivered",
};

function formatWhen(iso: string | null): string {
  if (!iso) return "";
  return new Date(iso).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" });
}

export function OrderTimeline({ currentStatus, history }: { currentStatus: OrderStatus; history: OrderStatusEvent[] }) {
  const reducedMotion = useReducedMotion();

  if (currentStatus === "CANCELLED") {
    const cancelEvent = history.find((h) => h.newStatus === "CANCELLED");
    return (
      <div className="flex items-center gap-3 rounded-2xl border border-red-100 bg-red-50/60 p-4">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-red-100 text-red-600">
          <X className="h-4 w-4" />
        </div>
        <div>
          <p className="font-medium text-red-700">Order cancelled</p>
          {cancelEvent?.changeReason && <p className="text-sm text-red-600">{cancelEvent.changeReason}</p>}
          <p className="text-xs text-red-400">{formatWhen(cancelEvent?.changedAt ?? null)}</p>
        </div>
      </div>
    );
  }

  const currentIndex = ORDER_STATUS_SEQUENCE.indexOf(currentStatus as (typeof ORDER_STATUS_SEQUENCE)[number]);
  const eventByStatus = new Map(history.map((h) => [h.newStatus, h]));

  return (
    <ol className="relative">
      {ORDER_STATUS_SEQUENCE.map((step, index) => {
        const isDone = index <= currentIndex;
        const isCurrent = index === currentIndex;
        const event = eventByStatus.get(step);
        const isLast = index === ORDER_STATUS_SEQUENCE.length - 1;

        return (
          <li key={step} className="relative flex gap-4 pb-8 last:pb-0">
            {!isLast && (
              <span
                className={cn("absolute left-[15px] top-8 h-full w-px", isDone ? "bg-[#5b4ef9]" : "bg-slate-200")}
                aria-hidden
              />
            )}
            <motion.div
              initial={reducedMotion ? { opacity: 0 } : { opacity: 0, scale: 0.6 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: reducedMotion ? 0 : index * 0.05, type: "spring", stiffness: 400, damping: 24 }}
              className={cn(
                "z-10 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2",
                isDone ? "border-[#5b4ef9] bg-[#5b4ef9] text-white" : "border-slate-200 bg-white text-slate-300",
                isCurrent && !reducedMotion && "ring-4 ring-[#5b4ef9]/15",
              )}
            >
              {isDone ? <Check className="h-4 w-4" /> : <span className="h-2 w-2 rounded-full bg-current" />}
            </motion.div>
            <div className="pt-1">
              <p className={cn("text-sm font-medium", isDone ? "text-slate-900" : "text-slate-400")}>{STEP_LABELS[step]}</p>
              {event && <p className="text-xs text-slate-400">{formatWhen(event.changedAt)}</p>}
            </div>
          </li>
        );
      })}
    </ol>
  );
}

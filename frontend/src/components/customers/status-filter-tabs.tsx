"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { CUSTOMER_STATUSES, type CustomerStatus } from "@/lib/api/customers";

export type StatusFilterValue = "ALL" | CustomerStatus;

const TABS: { value: StatusFilterValue; label: string }[] = [
  { value: "ALL", label: "All" },
  ...CUSTOMER_STATUSES.map((s) => ({
    value: s,
    label: s.charAt(0) + s.slice(1).toLowerCase(),
  })),
];

export function StatusFilterTabs({
  value,
  onChange,
}: {
  value: StatusFilterValue;
  onChange: (value: StatusFilterValue) => void;
}) {
  return (
    <div className="inline-flex items-center gap-1 rounded-full border border-slate-200 bg-white p-1 shadow-sm">
      {TABS.map((tab) => {
        const active = tab.value === value;
        return (
          <button
            key={tab.value}
            type="button"
            onClick={() => onChange(tab.value)}
            className={cn(
              "relative rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors",
              active ? "text-white" : "text-slate-600 hover:text-slate-900",
            )}
          >
            {active && (
              <motion.span
                layoutId="customer-status-tab-indicator"
                className="absolute inset-0 rounded-full bg-[#5b4ef9]"
                transition={{ type: "spring", stiffness: 500, damping: 35 }}
              />
            )}
            <span className="relative z-10">{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
}

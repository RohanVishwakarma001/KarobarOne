"use client";

import * as React from "react";
import { AnimatePresence, motion, useAnimationControls } from "framer-motion";
import { AlertCircle, Check, Loader2 } from "lucide-react";
import { Button, buttonVariants } from "./button";
import { cn } from "./utils";
import { springs, useReducedMotion } from "@/lib/motion";
import type { VariantProps } from "class-variance-authority";

/** Matches TanStack Query's `mutation.status` naming 1:1 so callers can pass it straight through. */
export type AsyncButtonStatus = "idle" | "pending" | "success" | "error";

export type AnimatedButtonProps = Omit<React.ComponentProps<"button">, "children"> &
  VariantProps<typeof buttonVariants> & {
    status: AsyncButtonStatus;
    /** Default label, shown whenever status is "idle" (also the disabled/pending fallback if no separate label given). */
    label: React.ReactNode;
    icon?: React.ReactNode;
    loadingLabel?: React.ReactNode;
    successLabel?: React.ReactNode;
    errorLabel?: React.ReactNode;
    /** How long the success/error flash holds before reverting to idle. Default 1600ms. */
    resetAfterMs?: number;
  };

/**
 * A submit/save button that morphs through Idle -> Spinner -> Checkmark (or
 * an error shake) instead of just disabling/re-enabling. Drive it with a
 * mutation's `status` — the button owns its own success/error *display*
 * timer internally, so the parent doesn't need to call `mutation.reset()`
 * for the checkmark to go away.
 */
export function AnimatedButton({
  status,
  label,
  icon,
  loadingLabel,
  successLabel = "Saved",
  errorLabel = "Failed",
  resetAfterMs = 1600,
  className,
  variant,
  size,
  disabled,
  ...props
}: AnimatedButtonProps) {
  const reducedMotion = useReducedMotion();
  const [display, setDisplay] = React.useState<AsyncButtonStatus>("idle");
  const shakeControls = useAnimationControls();

  React.useEffect(() => {
    setDisplay(status);
    if (status === "success" || status === "error") {
      const timer = setTimeout(() => setDisplay("idle"), resetAfterMs);
      return () => clearTimeout(timer);
    }
  }, [status, resetAfterMs]);

  React.useEffect(() => {
    if (display === "error" && !reducedMotion) {
      shakeControls.start({ x: [0, -7, 7, -5, 5, -2, 2, 0], transition: { duration: 0.45, ease: "easeInOut" } });
    }
  }, [display, reducedMotion, shakeControls]);

  const content = {
    idle: { key: "idle", node: <>{icon}{label}</>, tone: "" },
    pending: { key: "pending", node: <>{<Loader2 className="h-4 w-4 animate-spin" />}{loadingLabel ?? label}</>, tone: "" },
    success: { key: "success", node: <>{<Check className="h-4 w-4" />}{successLabel}</>, tone: "bg-emerald-600 hover:bg-emerald-600" },
    error: { key: "error", node: <>{<AlertCircle className="h-4 w-4" />}{errorLabel}</>, tone: "bg-red-600 hover:bg-red-600" },
  }[display];

  return (
    <motion.span animate={shakeControls} className="inline-block">
      <Button
        type={display === "idle" ? props.type : "button"}
        variant={variant}
        size={size}
        disabled={disabled || display === "pending"}
        className={cn("relative overflow-hidden transition-colors", content.tone, className)}
        {...props}
      >
        <AnimatePresence mode="wait" initial={false}>
          <motion.span
            key={content.key}
            initial={reducedMotion ? { opacity: 0 } : { opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={reducedMotion ? { opacity: 0 } : { opacity: 0, y: -6 }}
            transition={reducedMotion ? { duration: 0.1 } : springs.snappy}
            className="inline-flex items-center gap-2"
          >
            {content.node}
          </motion.span>
        </AnimatePresence>
      </Button>
    </motion.span>
  );
}

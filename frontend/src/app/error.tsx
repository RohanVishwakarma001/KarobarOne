"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { AlertTriangle, Home, RotateCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { springs, useReducedMotion } from "@/lib/motion";

/**
 * Route-segment error boundary — catches a render/data error anywhere under
 * this segment without taking down the whole app (global-error.tsx is the
 * only-if-the-root-layout-itself-throws fallback, a much rarer case).
 */
export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const reducedMotion = useReducedMotion();
  const [isRetrying, setIsRetrying] = useState(false);

  useEffect(() => {
    // Server-side error logging hook — this app has no client error-tracking
    // service wired up yet, so this is the one place a caught render error
    // is currently visible at all; console.error keeps it out of silent-fail territory.
    console.error("Route error boundary caught:", error);
  }, [error]);

  const handleRetry = () => {
    setIsRetrying(true);
    // reset() re-renders the segment; if it throws again this component
    // remounts with a fresh error, so isRetrying naturally resets via the
    // component key changing — no need to manually flip it back off here.
    reset();
  };

  return (
    <div className="flex min-h-[70vh] items-center justify-center px-4 py-16">
      <motion.div
        initial={reducedMotion ? { opacity: 0 } : { opacity: 0, y: 16, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={reducedMotion ? { duration: 0.15 } : springs.gentle}
        className="flex max-w-md flex-col items-center text-center"
      >
        <motion.div
          animate={reducedMotion ? {} : { rotate: [0, -6, 6, -4, 4, 0] }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="flex h-16 w-16 items-center justify-center rounded-full bg-red-50 text-red-500"
        >
          <AlertTriangle className="h-8 w-8" />
        </motion.div>

        <h1 className="mt-6 text-xl font-semibold text-slate-900">Something went wrong</h1>
        <p className="mt-2 text-sm text-slate-500">
          An unexpected error occurred while loading this page. You can try again, or head back home.
        </p>
        {error.digest && (
          <p className="mt-2 font-mono text-xs text-slate-400">Reference: {error.digest}</p>
        )}

        <div className="mt-6 flex items-center gap-3">
          <Button onClick={handleRetry} className="gap-2 bg-[#5b4ef9] hover:bg-[#4a3ee0]">
            <motion.span
              animate={isRetrying && !reducedMotion ? { rotate: 360 } : { rotate: 0 }}
              transition={{ duration: 0.6, ease: "linear", repeat: isRetrying ? Infinity : 0 }}
              className="inline-flex"
            >
              <RotateCw className="h-4 w-4" />
            </motion.span>
            Try again
          </Button>
          <Link href="/">
            <Button variant="outline" className="gap-2">
              <Home className="h-4 w-4" />
              Go home
            </Button>
          </Link>
        </div>
      </motion.div>
    </div>
  );
}

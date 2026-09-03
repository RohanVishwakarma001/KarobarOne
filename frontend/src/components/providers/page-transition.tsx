"use client";

import { usePathname } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";
import { pageTransition, pageVariants, useReducedMotion } from "@/lib/motion";

/**
 * Seamless page-to-page transition for a layout segment. Keyed by pathname
 * so AnimatePresence treats each route as a distinct element — the outgoing
 * page fades/settles out while the incoming one fades/settles in, instead of
 * the default hard cut. Scoped to the store-owner-dashboard layout rather
 * than the root layout so it only touches the screens built this session,
 * not the marketing/mockup routes elsewhere in the app.
 */
export function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const reducedMotion = useReducedMotion();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        variants={reducedMotion ? undefined : pageVariants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={reducedMotion ? { duration: 0.12 } : pageTransition}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
